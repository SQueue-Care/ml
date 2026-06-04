# Baseline Model Evaluation & Error Analysis Report

## 🏥 SmartQueue AI — Laporan Kinerja Model Baseline

**Dokumen Kontrol:**
*   **Proyek:** SmartQueue AI Capstone
*   **Model Baseline:** Linear Regression (Ordinary Least Squares)
*   **Data Pembagian (Split):** TimeSeriesSplit (Split Final)
*   **Metrik Evaluasi:** MAE, RMSE, R² (Real Minutes)
*   **Status Dokumen:** Final & Terverifikasi

---

## 1. Ringkasan Eksekutif (Executive Summary)

Sebagai bagian penting dari siklus pengembangan model pembelajaran mesin (*machine learning lifecycle*) untuk memprediksi waktu tunggu pasien rumah sakit, model dasar (*baseline model*) menggunakan **Linear Regression** telah diimplementasikan, dilatih, dan dievaluasi. Laporan ini menyajikan kinerja empiris dari model baseline tersebut, mengidentifikasi titik lemah struktural melalui analisis kesalahan (*error analysis*), serta memberikan pembenaran ilmiah atas transisi ke arsitektur non-linear yang lebih kompleks seperti XGBoost dan Custom Deep Learning dengan residual blocks.

---

## 2. Metodologi Pelatihan & Pembagian Data

Untuk mencegah kebocoran data masa depan ke masa lalu (*data leakage*), data dibagi secara kronologis menggunakan metode **TimeSeriesSplit** dengan $n\_splits=5$. 

### 2.1 Fitur yang Digunakan
Model baseline dilatih menggunakan 13 fitur terstandarisasi yang diekstrak secara kronologis:
*   **Karakteristik Pasien:** `umur`, `asuransi_enc`, `prioritas_enc`, `status_pasien_enc`
*   **Keadaan Operasional:** `jumlah_antrian`, `jam_kedatangan`, `nama_poli_enc`, `is_peak`
*   **Dimensi Temporal:** `day_of_week`, `month`, `week_of_year`, `hour_sin`, `hour_cos`

### 2.2 Penyekalaan Fitur (Scaling)
*   **Fitur Input ($X$):** Ditransformasikan menggunakan `StandardScaler` yang disesuaikan hanya pada data latih (*fit only on training split*).
*   **Variabel Target ($y$):** Ditransformasikan menggunakan `MinMaxScaler` ke rentang $[0, 1]$ untuk menjaga konsistensi prapemrosesan dengan model Deep Learning. Semua hasil metrik evaluasi telah dikembalikan ke satuan waktu aslinya (**menit**) sebelum dihitung.

---

## 3. Kinerja Model Baseline (Evaluation Metrics)

Setelah dilakukan prediksi pada data uji independen (final split), didapatkan metrik performa baseline dalam satuan **menit riil** sebagai berikut:

| Metrik | Deskripsi | Nilai (Menit Riil) | Interpretasi |
| :--- | :--- | :--- | :--- |
| **MAE** | Mean Absolute Error | **3.388407** | Rata-rata absolut kesalahan prediksi model adalah sekitar **3 menit 23 detik**. |
| **RMSE** | Root Mean Squared Error | **4.366500** | Kesalahan kuadrat rata-rata model adalah **4 menit 22 detik**. Selisih yang relatif kecil dengan MAE mengindikasikan jarangnya outlier ekstrem. |
| **R²** | Coefficient of Determination | **0.932950** | Model baseline mampu menjelaskan **93.29%** variansi dari waktu tunggu pasien di data uji. |

---

## 4. Analisis Kesalahan Sistematis (Detailed Error Analysis)

Analisis mendalam dilakukan dengan membedah nilai MAE berdasarkan segmentasi operasional untuk mengidentifikasi area kegagalan struktural model linear:

### 4.1 Segmentasi Berdasarkan Poli Klinik (Clinic Department)
Poli Penyakit Dalam menunjukkan tingkat kesalahan prediksi tertinggi, diikuti oleh Poli Umum dan Poli Gigi:

| Nama Poli | MAE (Menit) | Karakteristik Operasional |
| :--- | :--- | :--- |
| **Poli Penyakit Dalam** | **4.1531** | Variabilitas durasi pelayanan tinggi karena kompleksitas diagnosis pasien. |
| **Poli Umum** | **3.4285** | Beban antrean tinggi pada jam-jam tertentu. |
| **Poli Gigi** | **3.4275** | Prosedur penanganan medis yang bervariasi. |
| **Poli Anak** | **3.1999** | Interaksi pasien anak yang membutuhkan waktu penanganan dinamis. |
| **Poli Jantung** | **3.1427** | Penjadwalan spesifik yang memengaruhi pola tunggu. |
| **Poli Kandungan** | **3.0017** | Alur pemeriksaan rutin yang relatif lebih terprediksi. |

### 4.2 Segmentasi Berdasarkan Prioritas Pasien (Patient Priority)
Ditemukan bias kesalahan yang sangat timpang berdasarkan tingkat kedaruratan pasien:
*   **Urgent (Kategori Kedaruratan Tinggi):** MAE mencapai **5.8746 menit** (Kesalahan rata-rata hampir 6 menit).
*   **Normal:** MAE hanya **2.9681 menit** (Di bawah 3 menit).

> [!WARNING]
> **Kelemahan Kritis Model Linear:** 
> Model Linear Regression gagal menangkap prioritas kedaruratan secara dinamis. Pasien berkategori *Urgent* yang secara operasional langsung dipotong antreannya memiliki waktu tunggu aktual yang sangat singkat secara non-linear. Asumsi hubungan linear pada fitur prioritas mengakibatkan model linear secara konsisten memprediksi waktu tunggu yang terlalu lama bagi pasien darurat.

### 4.3 Segmentasi Jam Sibuk vs Jam Biasa (Temporal Load Peak)
*   **Normal Hours (`is_peak=0`):** MAE **2.6573 menit**
*   **Peak Hours (`is_peak=1`):** MAE **3.7938 menit**

Saat beban rumah sakit tinggi (Jam Sibuk pukul 08:00 - 11:00), kesalahan prediksi meningkat sebesar **42.7%**. Hal ini menunjukkan ketidakmampuan model linear dalam merepresentasikan efek antrean yang menumpuk secara eksponensial selama jam sibuk.

---

## 5. Kelemahan Struktural Model Baseline & Rekomendasi

Berdasarkan visualisasi grafik distribusi sisa (*residual plot*) dan scatter plot pada `deployment/model/baseline_error_analysis.png`, ditemukan beberapa kelemahan mendasar:

1.  **Kegagalan Distribusi Sisa (Residual Skewness):** Distribusi residual memperlihatkan kemiringan (*skewness*) asimetris di sekitar angka nol, menunjukkan adanya bias sistematis di mana model linear sering kali melakukan *under-prediction* pada beban kerja puncak.
2.  **Efek Antrean Non-Linear:** Hubungan antara jumlah orang dalam antrean dengan waktu tunggu sebenarnya tidak murni linear karena adanya interaksi efisiensi staf medis dan waktu istirahat yang tidak konstan.
3.  **Tindakan Prioritas Asimetris:** Hubungan prioritas kedaruratan bersifat diskrit dan memengaruhi antrean secara asimetris, yang tidak dapat dipetakan dengan baik oleh persamaan linear regresi multivariat konvensional.

---

## 6. Kesimpulan & Justifikasi Upgrade Model

Meskipun model baseline Linear Regression menghasilkan nilai $R^2$ yang tergolong tinggi (93.29%) karena tren umum antrean yang linear, model ini **gagal total** dalam memberikan prediksi yang andal untuk kelompok krusial, yaitu **pasien Urgent** dan **situasi Jam Sibuk (Peak Hours)**. 

Oleh karena itu, sangat direkomendasikan untuk menerapkan model non-linear:
*   **XGBoost Regressor** (yang menghasilkan MAE lebih baik yaitu **2.55 menit**) untuk performa operasional cepat.
*   **Custom Functional Keras Neural Network** dengan **Residual Dense Blocks** dan **Weighted Huber Loss** (MAE **2.89 menit** dengan garansi asimetris) untuk memberikan penalti asimetris terhadap *under-prediction*, sehingga menjamin kepuasan pasien saat sistem diimplementasikan di lingkungan produksi.
