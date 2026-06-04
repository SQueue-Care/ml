import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Literal

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator


class ResidualDenseBlock(layers.Layer):
    def __init__(self, units, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.units        = units
        self.dropout_rate = dropout_rate
        self.dense        = layers.Dense(units, use_bias=False)
        self.batch_norm   = layers.BatchNormalization()
        self.activation   = layers.Activation("relu")
        self.dropout      = layers.Dropout(dropout_rate)
        self.projection   = None

    def build(self, input_shape):
        if input_shape[-1] != self.units:
            self.projection = layers.Dense(
                self.units, use_bias=False,
                name=f"{self.name}_projection"
            )
        super().build(input_shape)

    def call(self, inputs, training=False):
        x        = self.dense(inputs)
        x        = self.batch_norm(x, training=training)
        x        = self.activation(x)
        x        = self.dropout(x, training=training)
        residual = self.projection(inputs) if self.projection else inputs
        return x + residual

    def get_config(self):
        cfg = super().get_config()
        cfg.update({"units": self.units, "dropout_rate": self.dropout_rate})
        return cfg


class WeightedHuberLoss(keras.losses.Loss):
    def __init__(self, delta=0.1, urgent_weight=2.0,
                 name="weighted_huber_loss", **kwargs):
        super().__init__(name=name, **kwargs)
        self.delta         = delta
        self.urgent_weight = urgent_weight

    def call(self, y_true, y_pred, sample_weight=None):
        y_true = tf.cast(y_true, tf.float32)
        y_pred = tf.cast(y_pred, tf.float32)
        error  = y_true - y_pred
        abs_e  = tf.abs(error)
        huber  = tf.where(
            abs_e <= self.delta,
            0.5 * tf.square(error),
            self.delta * (abs_e - 0.5 * self.delta)
        )
        if sample_weight is not None:
            sw    = tf.cast(tf.reshape(sample_weight, [-1]), tf.float32)
            huber = huber * sw
        return tf.reduce_mean(huber)

    def get_config(self):
        cfg = super().get_config()
        cfg.update({"delta": self.delta, "urgent_weight": self.urgent_weight})
        return cfg


# Konstanta encoding — harus konsisten dengan dataset training

ASURANSI_MAP = {
    "bpjs": 0,
    "umum": 1,
}

PRIORITAS_MAP = {
    "normal": 0,
    "urgent": 1,
}

POLI_MAP = {
    "anak"          : 0,
    "gigi"          : 1,
    "jantung"       : 2,
    "kandungan"     : 3,
    "penyakit dalam": 4,
    "umum"          : 5,
}

HARI_MAP = {
    "monday"   : 0,
    "tuesday"  : 1,
    "wednesday": 2,
    "thursday" : 3,
    "friday"   : 4,
    "saturday" : 5,
    "sunday"   : 6,
}

# Normalisasi target (y_min, y_max dari training)
Y_MIN = 0.0
Y_MAX = 87.0

# Path artifacts
MODEL_PATH  = os.getenv("MODEL_PATH",  "models/model_smartqueue.keras")
SCALER_PATH = os.getenv("SCALER_PATH", "models/scaler.pkl")

FITUR_NUMERIK = ["umur", "jumlah_antrian", "jam_kedatangan"]


# Global state — model & scaler dimuat sekali saat startup

class ModelState:
    model : keras.Model = None
    scaler              = None


state = ModelState()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load model & scaler saat startup, cleanup saat shutdown."""
    print("[startup] Memuat model SmartQueue AI...")
    try:
        state.model = keras.models.load_model(
            MODEL_PATH,
            custom_objects={
                "ResidualDenseBlock": ResidualDenseBlock,
                "WeightedHuberLoss" : WeightedHuberLoss,
            }
        )
        state.scaler = joblib.load(SCALER_PATH)

        # Validasi input shape — harus (None, 9) — tanpa status_pasien
        expected_dim = 9
        actual_dim   = state.model.input_shape[-1]
        if actual_dim != expected_dim:
            raise ValueError(
                f"Model input shape salah: expected (None, {expected_dim}), "
                f"got {state.model.input_shape}. "
                f"Pastikan file models/model_smartqueue.keras adalah hasil "
                f"training terbaru (tanpa fitur status_pasien)."
            )

        # Validasi scaler — harus fit dengan 3 fitur numerik
        expected_scaler_features = 3
        if hasattr(state.scaler, 'n_features_in_') and state.scaler.n_features_in_ != expected_scaler_features:
            raise ValueError(
                f"Scaler salah: expected {expected_scaler_features} fitur, "
                f"got {state.scaler.n_features_in_}. "
                f"Pastikan scaler.pkl dari hasil training RS2 terbaru "
                f"(FITUR_NUMERIK = ['umur', 'jumlah_antrian', 'jam_kedatangan'])."
            )

        print(f"[startup] Model loaded    : {MODEL_PATH}")
        print(f"[startup] Scaler loaded   : {SCALER_PATH}")
        print(f"[startup] Input shape     : {state.model.input_shape}  ✓")
        print(f"[startup] Output shape    : {state.model.output_shape}")
    except Exception as e:
        print(f"[startup] ERROR: {e}")
        raise

    yield

    print("[shutdown] SmartQueue AI API berhenti.")



# FastAPI App

app = FastAPI(
    title       = "SmartQueue AI API",
    description = "Prediksi waktu tunggu pasien rumah sakit berbasis Deep Learning",
    version     = "1.0.0",
    lifespan    = lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*"],
    allow_credentials = True,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)



# Schema Request & Response

class PredictRequest(BaseModel):
    umur           : int   = Field(..., ge=1, le=120,  description="Umur pasien (tahun)", example=45)
    jumlah_antrian : int   = Field(..., ge=0, le=500,  description="Jumlah pasien dalam antrian saat ini", example=10)
    jam_kedatangan : int   = Field(..., ge=0, le=23,   description="Jam kedatangan pasien (0-23)", example=9)
    asuransi       : str   = Field(...,                description="Jenis asuransi: 'bpjs' atau 'umum'", example="bpjs")
    prioritas      : str   = Field(...,                description="Prioritas pasien: 'normal' atau 'urgent'", example="normal")
    nama_poli      : str   = Field(...,                description="Nama poli tujuan", example="umum")
    tanggal        : str   = Field(...,                description="Tanggal kunjungan (YYYY-MM-DD)", example="2025-06-01")

    @field_validator("asuransi")
    @classmethod
    def validate_asuransi(cls, v: str) -> str:
        v_lower = v.strip().lower()
        if v_lower not in ASURANSI_MAP:
            raise ValueError(f"asuransi harus 'bpjs' atau 'umum', diterima: '{v}'")
        return v_lower

    @field_validator("prioritas")
    @classmethod
    def validate_prioritas(cls, v: str) -> str:
        v_lower = v.strip().lower()
        if v_lower not in PRIORITAS_MAP:
            raise ValueError(f"prioritas harus 'normal' atau 'urgent', diterima: '{v}'")
        return v_lower

    @field_validator("nama_poli")
    @classmethod
    def validate_nama_poli(cls, v: str) -> str:
        v_lower = v.strip().lower()
        if v_lower not in POLI_MAP:
            valid = list(POLI_MAP.keys())
            raise ValueError(f"nama_poli tidak valid. Pilihan: {valid}, diterima: '{v}'")
        return v_lower

    @field_validator("tanggal")
    @classmethod
    def validate_tanggal(cls, v: str) -> str:
        try:
            datetime.strptime(v.strip(), "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"tanggal harus format YYYY-MM-DD, diterima: '{v}'")
        return v.strip()


class PredictResponse(BaseModel):
    predicted_waiting_time_minutes : float
    kategori_waktu_tunggu          : str
    status                         : str


class HealthResponse(BaseModel):
    status       : str
    model_loaded : bool
    version      : str



# Helper
# Mapping is_peak per jam — diambil langsung dari dataset training
# Jam 9-11 = peak (1), selain itu = non-peak (0)
_IS_PEAK_MAP = {7:0, 8:0, 9:1, 10:1, 11:1, 12:0, 13:0, 14:0}

def _is_peak(jam: int) -> int:
    """Konversi jam ke is_peak sesuai definisi di dataset training."""
    return _IS_PEAK_MAP.get(jam, 0)


def _hari_enc(tanggal_str: str) -> int:
    """Konversi tanggal ke encoding hari (0=Senin, 6=Minggu)."""
    dt   = datetime.strptime(tanggal_str, "%Y-%m-%d")
    nama = dt.strftime("%A").lower()
    return HARI_MAP.get(nama, 0)


def _denorm(y_norm: float) -> float:
    """Denormalisasi output sigmoid (0-1) ke menit."""
    return y_norm * (Y_MAX - Y_MIN) + Y_MIN


def _kategori(menit: float) -> str:
    if menit < 20:
        return "Cepat"
    elif menit < 45:
        return "Sedang"
    else:
        return "Lama"


def _build_input(req: PredictRequest) -> np.ndarray:

    # Numerik — scale
    X_num = state.scaler.transform(
        np.array([[req.umur, req.jumlah_antrian, req.jam_kedatangan]],
                 dtype=np.float32)
    ).astype(np.float32)

    # Encoded — 6 fitur, tanpa status_pasien_enc
    X_enc = np.array([[
        _is_peak(req.jam_kedatangan),   # is_peak
        0,                               # jenis_kelamin_enc (default P=0)
        _hari_enc(req.tanggal),         # hari_enc
        ASURANSI_MAP[req.asuransi],     # asuransi_enc
        PRIORITAS_MAP[req.prioritas],   # prioritas_enc
        POLI_MAP[req.nama_poli],        # nama_poli_enc
    ]], dtype=np.float32)

    return np.concatenate([X_num, X_enc], axis=1)


# ─────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────

@app.get("/", tags=["Root"])
def root():
    return {
        "service": "SmartQueue AI API",
        "version": "1.0.0",
        "docs"   : "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health():
    return HealthResponse(
        status       = "ok" if state.model is not None else "model_not_loaded",
        model_loaded = state.model is not None,
        version      = "1.0.0",
    )




@app.post("/debug", tags=["Debug"])
def debug_input(req: PredictRequest):
    """Endpoint debug — tampilkan nilai fitur yang masuk ke model."""
    from datetime import datetime as _dt
    X_in  = _build_input(req)
    pred_n = float(state.model(X_in, training=False).numpy().flatten()[0])
    pred_m = round(_denorm(pred_n), 2)

    wkt = _dt.strptime(req.tanggal, "%Y-%m-%d")
    return {
        "input_raw": {
            "umur"          : req.umur,
            "jumlah_antrian": req.jumlah_antrian,
            "jam_kedatangan": req.jam_kedatangan,
            "asuransi"      : req.asuransi,
            "prioritas"     : req.prioritas,
            "nama_poli"     : req.nama_poli,
            "tanggal"       : req.tanggal,
        },
        "encoded": {
            "is_peak"          : int(X_in[0][3]),
            "jenis_kelamin_enc": int(X_in[0][4]),
            "hari_enc"         : int(X_in[0][5]),
            "hari_name"        : wkt.strftime("%A"),
            "asuransi_enc"     : int(X_in[0][6]),
            "prioritas_enc"    : int(X_in[0][7]),
            "nama_poli_enc"    : int(X_in[0][8]),
        },
        "scaled_numerik": {
            "umur_scaled"          : round(float(X_in[0][0]), 6),
            "jumlah_antrian_scaled": round(float(X_in[0][1]), 6),
            "jam_kedatangan_scaled": round(float(X_in[0][2]), 6),
        },
        "x_in_full"   : X_in[0].tolist(),
        "x_in_shape"  : list(X_in.shape),
        "pred_n_raw"  : round(pred_n, 6),
        "pred_m_menit": pred_m,
    }

@app.post("/predict", response_model=PredictResponse, tags=["Prediction"])
def predict(req: PredictRequest):
    if state.model is None:
        raise HTTPException(status_code=503, detail="Model belum siap.")

    try:
        X_in   = _build_input(req)
        pred_n = float(state.model(X_in, training=False).numpy().flatten()[0])
        pred_m = round(_denorm(pred_n), 2)
        pred_m = max(0.0, pred_m)

        return PredictResponse(
            predicted_waiting_time_minutes = pred_m,
            kategori_waktu_tunggu          = _kategori(pred_m),
            status                         = "success",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")