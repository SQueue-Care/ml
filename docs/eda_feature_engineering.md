# EDA Collaboration & Feature Engineering Documentation

## Overview

Dokumen ini menjelaskan proses exploratory data analysis (EDA), feature engineering, validasi fitur, dan persiapan dataset training untuk project **SmartQueue AI**, yaitu sistem prediksi waktu tunggu pasien rumah sakit berbasis machine learning.

Tujuan utama proses ini adalah membangun pipeline data yang kuat untuk mendukung model prediksi antrean pasien secara akurat dan efisien.

---

# 1. Exploratory Data Analysis (EDA)

## Dataset Review

Analisis awal dilakukan untuk memahami:

* Struktur dataset
* Tipe data
* Missing values
* Distribusi fitur
* Korelasi antar variabel
* Outlier
* Pola operasional rumah sakit

## Key Findings

* Dataset relatif bersih tanpa missing values signifikan
* Peak hours meningkatkan waktu tunggu pasien
* Beberapa departemen memiliki beban antrean lebih tinggi
* Insurance type memengaruhi distribusi layanan
* Service duration memiliki korelasi tinggi terhadap wait time
* Doctor workload berpengaruh terhadap performa antrean

---

# 2. Temporal Feature Engineering

Fitur waktu dirancang untuk menangkap pola antrean berdasarkan waktu kunjungan pasien.

## Features:

* `arrival_hour`
* `day_of_week`
* `month`
* `week_of_year`
* `is_peak`
* `hour_sin`
* `hour_cos`
* `day_sin`
* `day_cos`

## Purpose:

* Menangkap pola harian
* Menangkap pola mingguan
* Menangkap peak operational hours
* Representasi cyclical time untuk machine learning

---

# 3. Queue-Based Feature Engineering

Fitur antrean dibuat untuk merepresentasikan dinamika operasional rumah sakit.

## Features:

* `queue_per_hour`
* `queue_trend`
* `queue_velocity`
* `dept_queue_load`
* `doctor_daily_load`
* `service_pressure`

## Purpose:

* Mengukur kepadatan antrean
* Mengukur perubahan antrean
* Mengukur kecepatan layanan
* Mengukur tekanan operasional real-time

---

# 4. Doctor-Based Features

## Features:

* `doctor_avg_wait`
* `doctor_daily_load`
* `doctor_efficiency`

## Purpose:

* Mengukur performa dokter
* Mengukur beban kerja dokter
* Mengidentifikasi bottleneck layanan

---

# 5. Department-Based Features

## Features:

* `dept_avg_wait`
* `dept_queue_load`
* `dept_service_capacity`

## Purpose:

* Mengukur kapasitas layanan departemen
* Mengidentifikasi unit dengan antrean tinggi
* Menambah konteks operasional sistem

---

# 6. Feature Validation

Validasi dilakukan menggunakan:

* Correlation heatmap
* Distribution plots
* Boxplots
* Scatterplots
* Operational analysis

## Outcome:

Fitur-fitur engineered menunjukkan hubungan signifikan dengan target variable `wait_time`, sehingga layak digunakan dalam model training.

---

# 7. Preprocessing Pipeline

## Steps:

1. Feature selection
2. Label encoding categorical variables
3. Numerical scaling using StandardScaler
4. Save preprocessing artifacts:

   * `scaler.save`
   * `label_encoders.save`

---

# 8. Final Selected Features

Total fitur final mencakup:

* Patient features
* Temporal features
* Queue features
* Doctor features
* Department features
* Operational pressure features

---

# 9. Deliverables

## Completed:

* Full EDA analysis
* Temporal feature engineering
* Queue feature engineering
* Doctor & department validation
* Feature engineering pipeline
* Feature documentation
* Prepared training dataset
* Scaler artifact
* Encoder artifact

---

# 10. Next Stage

Dataset dan pipeline ini akan digunakan untuk:

* Baseline ML model
* Deep Learning model
* TensorBoard optimization
* FastAPI deployment
* Dashboard integration

---

# Conclusion

Issue #10 berhasil menyelesaikan seluruh proses data preparation dan feature engineering yang menjadi fondasi utama SmartQueue AI, memastikan model dapat dibangun di atas data yang telah tervalidasi, terstruktur, dan siap produksi.
