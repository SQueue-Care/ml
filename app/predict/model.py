"""Custom Keras layers dan fungsi load model prediksi waktu tunggu."""

import os

import joblib
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

MODEL_PATH = os.getenv("MODEL_PATH", "deployment/model_smartqueue.keras")
SCALER_PATH = os.getenv("SCALER_PATH", "deployment/scaler.pkl")

# Normalisasi target (y_min, y_max dari training)
Y_MIN = 0.0
Y_MAX = 87.0

# Mapping encoding — harus konsisten dengan dataset training
ASURANSI_MAP = {"bpjs": 0, "umum": 1}
PRIORITAS_MAP = {"normal": 0, "urgent": 1}
POLI_MAP = {
    "anak": 0,
    "gigi": 1,
    "jantung": 2,
    "kandungan": 3,
    "penyakit dalam": 4,
    "umum": 5,
}
HARI_MAP = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}
_IS_PEAK_MAP = {7: 0, 8: 0, 9: 1, 10: 1, 11: 1, 12: 0, 13: 0, 14: 0}


class ResidualDenseBlock(layers.Layer):
    def __init__(self, units, dropout_rate=0.1, **kwargs):
        super().__init__(**kwargs)
        self.units = units
        self.dropout_rate = dropout_rate
        self.dense = layers.Dense(units, use_bias=False)
        self.batch_norm = layers.BatchNormalization()
        self.activation = layers.Activation("relu")
        self.dropout = layers.Dropout(dropout_rate)
        self.projection = None

    def build(self, input_shape):
        if input_shape[-1] != self.units:
            self.projection = layers.Dense(
                self.units, use_bias=False, name=f"{self.name}_projection"
            )
        super().build(input_shape)

    def call(self, inputs, training=False):
        x = self.dense(inputs)
        x = self.batch_norm(x, training=training)
        x = self.activation(x)
        x = self.dropout(x, training=training)
        residual = self.projection(inputs) if self.projection else inputs
        return x + residual

    def get_config(self):
        cfg = super().get_config()
        cfg.update({"units": self.units, "dropout_rate": self.dropout_rate})
        return cfg


class WeightedHuberLoss(keras.losses.Loss):
    def __init__(self, delta=0.1, urgent_weight=2.0, name="weighted_huber_loss", **kwargs):
        super().__init__(name=name, **kwargs)
        self.delta = delta
        self.urgent_weight = urgent_weight

    def call(self, y_true, y_pred, sample_weight=None):
        y_true = tf.cast(y_true, tf.float32)
        y_pred = tf.cast(y_pred, tf.float32)
        error = y_true - y_pred
        abs_e = tf.abs(error)
        huber = tf.where(
            abs_e <= self.delta,
            0.5 * tf.square(error),
            self.delta * (abs_e - 0.5 * self.delta),
        )
        if sample_weight is not None:
            sw = tf.cast(tf.reshape(sample_weight, [-1]), tf.float32)
            huber = huber * sw
        return tf.reduce_mean(huber)

    def get_config(self):
        cfg = super().get_config()
        cfg.update({"delta": self.delta, "urgent_weight": self.urgent_weight})
        return cfg


def load_model():
    """Load Keras model dan scaler dari disk."""
    model = keras.models.load_model(
        MODEL_PATH,
        custom_objects={
            "ResidualDenseBlock": ResidualDenseBlock,
            "WeightedHuberLoss": WeightedHuberLoss,
        },
    )
    scaler = joblib.load(SCALER_PATH)
    return model, scaler


def is_peak(jam: int) -> int:
    return _IS_PEAK_MAP.get(jam, 0)


def hari_enc(tanggal_str: str) -> int:
    from datetime import datetime
    dt = datetime.strptime(tanggal_str, "%Y-%m-%d")
    return HARI_MAP.get(dt.strftime("%A").lower(), 0)


def denorm(y_norm: float) -> float:
    return y_norm * (Y_MAX - Y_MIN) + Y_MIN


def kategori(menit: float) -> str:
    if menit < 20:
        return "Cepat"
    elif menit < 45:
        return "Sedang"
    else:
        return "Lama"


def build_input(req, scaler) -> np.ndarray:
    X_num = scaler.transform(
        np.array([[req.umur, req.jumlah_antrian, req.jam_kedatangan]], dtype=np.float32)
    ).astype(np.float32)

    X_enc = np.array(
        [[
            is_peak(req.jam_kedatangan),
            0,  # jenis_kelamin_enc (default P=0)
            hari_enc(req.tanggal),
            ASURANSI_MAP[req.asuransi],
            PRIORITAS_MAP[req.prioritas],
            POLI_MAP[req.nama_poli],
        ]],
        dtype=np.float32,
    )

    return np.concatenate([X_num, X_enc], axis=1)
