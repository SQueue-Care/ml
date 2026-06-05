# **SmartQueue AI — Machine Learning & CDSS Service**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-develop-red.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)

## **Deskripsi Proyek**

**SmartQueue AI** adalah layanan *machine learning* berbasis REST API yang dikembangkan sebagai bagian dari **Capstone Project Coding Camp DBS Foundation 2025**. Layanan ini menyediakan dua fitur utama berbasis AI:

1. **Prediksi Waktu Tunggu Pasien** — model *deep learning* yang memproyeksikan estimasi waktu tunggu berdasarkan kondisi antrian dan profil pasien.
2. **Clinical Decision Support System (CDSS)** — sistem rekomendasi diagnosis yang menganalisis gejala klinis dan memberikan kandidat penyakit beserta saran pemeriksaan lanjutan, didukung oleh **Google Gemini AI**.

## **Fitur Utama**

- 🧠 **Prediksi Waktu Tunggu (Deep Learning):** Model *neural network* dengan arsitektur *Residual Dense Block* yang memprediksi waktu tunggu pasien secara real-time berdasarkan jumlah antrian, poli, jam kedatangan, dan faktor lainnya.
- 🩺 **CDSS berbasis Gemini AI:** Analisis gejala pasien dan menghasilkan hingga 3 kandidat diagnosis dengan tingkat urgensi, *confidence score*, departemen rujukan, dan pemeriksaan lanjutan yang direkomendasikan.
- ⚡ **Auto Model Fallback:** Sistem tahan banting terhadap batas kuota Gemini API — jika model utama gagal, sistem otomatis beralih ke model cadangan tanpa *downtime*.
- 🔌 **REST API siap integrasi:** Dibangun dengan FastAPI, dilengkapi dokumentasi Swagger interaktif dan CORS support.

## **Arsitektur & Teknologi**

**Tech Stack yang Digunakan:**

- **API Framework:** Python, FastAPI, Uvicorn, Gunicorn
- **Deep Learning:** TensorFlow 2.x, Keras
- **ML Utilities:** Scikit-learn, Pandas, NumPy, Joblib
- **AI / LLM:** Google Gemini API (`google-generativeai`)
- **Deployment:** Cloud VPS / Azure App Service
- **Tools:** Git, GitHub, Postman

Link Model Ai : https://drive.google.com/drive/folders/1N48kWDc9rZ1_6FGKqeHNw5USVE4DrLY5?usp=drive_link

## **Panduan Instalasi & Setup**

**Prasyarat:**
- [Python](https://www.python.org/) versi **3.11** (TensorFlow tidak kompatibel dengan Python 3.13+)
- [Git](https://git-scm.com/)
- [Conda](https://docs.conda.io/) *(direkomendasikan)* atau `venv`

**Langkah-langkah:**

1. **Clone repositori ini:**
   ```bash
   git clone <url-repo-ini>
   cd ml
   ```

2. **Setup environment Python:**
   ```bash
   # Opsi A — conda (direkomendasikan)
   conda create -n smartqueue python=3.11
   conda activate smartqueue

   # Opsi B — venv
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   # venv\Scripts\activate    # Windows

   pip install -r requirements.txt
   ```

3. **Konfigurasi environment variable:**

   Buat file `.env` di root proyek:
   ```env
   GEMINI_API_KEY=isi_dengan_api_key_asli
   GEMINI_MODEL=gemini-2.5-flash
   ```

   > Dapatkan API key gratis di [Google AI Studio](https://aistudio.google.com/apikey).

## **Menjalankan Aplikasi**

```bash
uvicorn app.app:app --reload
```

- API berjalan di: `http://127.0.0.1:8000`
- Dokumentasi Swagger: `http://127.0.0.1:8000/docs`

## **Endpoint API**

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| `GET` | `/` | Status API |
| `GET` | `/health` | Health check (termasuk status model) |
| `POST` | `/predict/` | Prediksi waktu tunggu pasien |
| `POST` | `/predict/debug` | Debug nilai fitur yang masuk ke model |
| `POST` | `/cdss/recommend` | Rekomendasi diagnosis berdasarkan gejala |
| `GET` | `/cdss/health` | Status konektivitas Gemini API |

**Contoh Request `/predict/`:**
```json
{
  "umur": 45,
  "jumlah_antrian": 10,
  "jam_kedatangan": 9,
  "asuransi": "bpjs",
  "prioritas": "normal",
  "nama_poli": "umum",
  "tanggal": "2025-06-01"
}
```

**Contoh Request `/cdss/recommend`:**
```json
{
  "gejala": "demam tinggi sudah 3 hari, batuk kering, sesak napas",
  "umur": 45,
  "jenis_kelamin": "L"
}
```

## **Tim Pengembang (CC25-CF042)**

| ID | Nama | Peran | Status |
|----|------|-------|--------|
| CFCC223D6Y2279 | Bintang Wishnu Pradana | Full-Stack Web Developer | Aktif |
| CFCC559D6Y0373 | Muhammad Fais Avriody Daffa | Full-Stack Web Developer | Aktif |
| CDCC223D6Y0280 | M. Alan Daulay | Data Scientist | Aktif |
| CDCC223D6Y2250 | Galih Fathurahman Ardiansyah | Data Scientist | Aktif |
| CACC559D6Y1659 | Khairul Anuar | AI Engineer | Aktif |
| CACC223D6Y0439 | Sulthon Aqthoris Sama | AI Engineer | Aktif |

---

> **⚠️ Disclaimer:** Fitur CDSS merupakan alat bantu berbasis AI dan **BUKAN** pengganti diagnosis medis. Keputusan klinis tetap sepenuhnya berada di tangan dokter yang merawat.

---

### **Lisensi**
Proyek ini dilisensikan di bawah [Lisensi MIT](./LICENSE).
