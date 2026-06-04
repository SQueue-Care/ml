"""Router FastAPI untuk endpoint prediksi waktu tunggu pasien."""

from datetime import datetime

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from app.predict.model import (
    ASURANSI_MAP,
    POLI_MAP,
    PRIORITAS_MAP,
    build_input,
    denorm,
    hari_enc,
    is_peak,
    kategori,
)

predict_router = APIRouter(prefix="/predict", tags=["Prediksi Waktu Tunggu"])


# ── State global model ──────────────────────────────────────────
class _State:
    model = None
    scaler = None


state = _State()


def init_model(model, scaler):
    """Dipanggil dari lifespan app utama saat startup."""
    state.model = model
    state.scaler = scaler


# ── Schemas ──────────────────────────────────────────────────────
class PredictRequest(BaseModel):
    umur: int = Field(..., ge=1, le=120, description="Umur pasien (tahun)", example=45)
    jumlah_antrian: int = Field(..., ge=0, le=500, description="Jumlah pasien dalam antrian", example=10)
    jam_kedatangan: int = Field(..., ge=0, le=23, description="Jam kedatangan pasien (0-23)", example=9)
    asuransi: str = Field(..., description="Jenis asuransi: 'bpjs' atau 'umum'", example="bpjs")
    prioritas: str = Field(..., description="Prioritas pasien: 'normal' atau 'urgent'", example="normal")
    nama_poli: str = Field(..., description="Nama poli tujuan", example="umum")
    tanggal: str = Field(..., description="Tanggal kunjungan (YYYY-MM-DD)", example="2025-06-01")

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
            raise ValueError(f"nama_poli tidak valid. Pilihan: {list(POLI_MAP.keys())}, diterima: '{v}'")
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
    predicted_waiting_time_minutes: float
    kategori_waktu_tunggu: str
    status: str


# ── Endpoints ────────────────────────────────────────────────────
@predict_router.post("/", response_model=PredictResponse, summary="Prediksi waktu tunggu pasien")
def predict(req: PredictRequest):
    if state.model is None:
        raise HTTPException(status_code=503, detail="Model belum siap.")
    try:
        X_in = build_input(req, state.scaler)
        pred_n = float(state.model(X_in, training=False).numpy().flatten()[0])
        pred_m = max(0.0, round(denorm(pred_n), 2))
        return PredictResponse(
            predicted_waiting_time_minutes=pred_m,
            kategori_waktu_tunggu=kategori(pred_m),
            status="success",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {e}")


@predict_router.post("/debug", summary="Debug nilai fitur yang masuk ke model")
def debug_input(req: PredictRequest):
    if state.model is None:
        raise HTTPException(status_code=503, detail="Model belum siap.")
    X_in = build_input(req, state.scaler)
    pred_n = float(state.model(X_in, training=False).numpy().flatten()[0])
    pred_m = round(denorm(pred_n), 2)
    dt = datetime.strptime(req.tanggal, "%Y-%m-%d")
    return {
        "input_raw": req.model_dump(),
        "encoded": {
            "is_peak": int(X_in[0][3]),
            "jenis_kelamin_enc": int(X_in[0][4]),
            "hari_enc": int(X_in[0][5]),
            "hari_name": dt.strftime("%A"),
            "asuransi_enc": int(X_in[0][6]),
            "prioritas_enc": int(X_in[0][7]),
            "nama_poli_enc": int(X_in[0][8]),
        },
        "scaled_numerik": {
            "umur_scaled": round(float(X_in[0][0]), 6),
            "jumlah_antrian_scaled": round(float(X_in[0][1]), 6),
            "jam_kedatangan_scaled": round(float(X_in[0][2]), 6),
        },
        "pred_n_raw": round(pred_n, 6),
        "pred_m_menit": pred_m,
    }
