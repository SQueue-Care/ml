"""Pydantic schemas untuk request dan response CDSS."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class CDSSRequest(BaseModel):
    """Schema request untuk rekomendasi penyakit berdasarkan gejala."""

    gejala: str = Field(
        min_length=3,
        description="Deskripsi gejala pasien dalam teks bebas (Bahasa Indonesia).",
    )
    umur: Optional[int] = Field(
        default=None,
        ge=0,
        le=120,
        description="Usia pasien (opsional, untuk konteks diagnosis).",
    )
    jenis_kelamin: Optional[str] = Field(
        default=None,
        description="Jenis kelamin pasien: 'L' atau 'P' (opsional).",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "gejala": "demam tinggi sudah 3 hari, batuk kering, sesak napas, nyeri dada saat bernapas",
                "umur": 45,
                "jenis_kelamin": "L",
            }
        }
    )


class KandidatDiagnosis(BaseModel):
    """Detail satu kandidat diagnosis."""

    nama_penyakit: str = Field(description="Nama penyakit yang direkomendasikan.")
    tingkat_urgensi: str = Field(
        description="Tingkat urgensi: 'LOW', 'MEDIUM', atau 'HIGH'."
    )
    confidence: int = Field(
        description="Tingkat keyakinan prediksi dalam bentuk persentase (1-100)."
    )
    departemen: str = Field(
        description="Departemen terkait, contoh: 'UMUM', 'BEDAH', 'PENYAKIT DALAM'."
    )
    penjelasan: str = Field(
        description="Penjelasan singkat mengapa penyakit ini direkomendasikan."
    )
    pemeriksaan_lanjutan: List[str] = Field(
        default=[],
        description="Daftar saran pemeriksaan lanjutan yang relevan."
    )


class CDSSResponse(BaseModel):
    """Schema response rekomendasi penyakit."""

    gejala_teridentifikasi: List[str] = Field(
        description="Daftar frasa gejala utama yang teridentifikasi dari input."
    )
    kandidat_diagnosis: List[KandidatDiagnosis] = Field(
        description="Daftar kandidat diagnosis (maksimal 3)."
    )
    catatan_medis: str = Field(
        description="Catatan dan saran medis tambahan dari sistem."
    )
    disclaimer: str = Field(
        default=(
            "Hasil ini merupakan rekomendasi berbasis AI dan BUKAN diagnosis medis. "
            "Keputusan klinis tetap sepenuhnya berada di tangan dokter yang menangani."
        ),
        description="Disclaimer wajib bahwa ini bukan diagnosis.",
    )
    status: str = "success"


class DoctorState(BaseModel):
    """Representasi status terkini seorang dokter."""

    id: str = Field(description="ID unik dokter.")
    nama: str = Field(description="Nama lengkap dokter.")
    nama_poli: str = Field(description="Departemen/poli dokter (contoh: 'umum', 'anak').")
    current_queue_length: int = Field(ge=0, description="Panjang antrean saat ini.")
    max_capacity: int = Field(gt=0, description="Kapasitas antrean maksimum.")
    avg_service_time: float = Field(gt=0.0, description="Rata-rata durasi layanan per pasien (menit).")
    efficiency_rating: float = Field(default=1.0, gt=0.0, description="Peringkat efisiensi dokter (default 1.0).")
    years_experience: int = Field(default=0, ge=0, description="Tahun pengalaman praktek.")
    active: bool = Field(default=True, description="Status keaktifan hari ini.")
    jam_mulai_praktek: Optional[str] = Field(default=None, description="Format HH:MM (contoh: '08:00').")
    jam_selesai_praktek: Optional[str] = Field(default=None, description="Format HH:MM (contoh: '14:00').")


class PatientProfile(BaseModel):
    """Representasi data profil klinis/personal pasien."""

    id: str = Field(description="ID unik pasien.")
    umur: float = Field(gt=0, le=120, description="Usia pasien.")
    asuransi: str = Field(description="Asuransi pasien ('bpjs' atau 'umum').")
    prioritas: str = Field(description="Prioritas antrean ('normal', 'rendah', 'sedang', 'urgent', 'tinggi', 'darurat').")
    status_pasien: str = Field(description="Status kunjungan ('rawat inap' atau 'rawat jalan').")
    nama_poli: str = Field(description="Nama departemen/poli rujukan.")
    preferred_doctor_id: Optional[str] = Field(default=None, description="ID dokter pilihan pasien (opsional).")
    tanggal: Optional[str] = Field(default=None, description="Format YYYY-MM-DD (opsional, jika kosong memakai hari ini).")


class PatientDistributionRequest(BaseModel):
    """Schema request untuk evaluasi distribusi pasien."""

    patient: PatientProfile = Field(description="Data profil pasien.")
    doctors: List[DoctorState] = Field(description="Daftar status dokter yang bertugas.")
    current_time: Optional[str] = Field(default=None, description="Format HH:MM (opsional, untuk mengecek jam praktek).")


class RecommendationDetail(BaseModel):
    """Detail rekomendasi hasil penilaian perutean."""

    doctor_id: str = Field(description="ID dokter yang dievaluasi.")
    doctor_name: str = Field(description="Nama dokter.")
    predicted_waiting_time_minutes: float = Field(description="Estimasi waktu tunggu dalam menit.")
    kategori_waktu_tunggu: str = Field(description="Kategori kelamaan waktu tunggu.")
    score_breakdown: Dict[str, float] = Field(description="Detail rincian skor komparasi.")
    queue_length: int = Field(description="Panjang antrean saat ini.")
    max_capacity: int = Field(description="Kapasitas maksimum.")


class PatientDistributionResponse(BaseModel):
    """Schema response dari perutean distribusi pasien."""

    recommended_doctor: RecommendationDetail = Field(description="Rekomendasi dokter utama paling optimal.")
    alternatives: List[RecommendationDetail] = Field(default=[], description="Daftar alternatif rujukan seimbang.")
    routing_mode: str = Field(description="Algoritma aktif: 'TSR' (Two-Stage Routing) atau 'fallback_wlb'.")
    latency_ms: float = Field(description="Durasi latensi proses kalkulasi dalam milidetik.")
    timestamp: str = Field(description="Waktu pemrosesan rekomendasi.")
    status: str = "success"
