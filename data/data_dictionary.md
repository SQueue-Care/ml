### Data Dictionary - Hospital Dataset

| Nama Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| `id_kunjungan` | String | ID unik untuk setiap kunjungan pasien. |
| `tanggal` | Datetime | Tanggal dilakukannya kunjungan. |
| `umur` | Float | Usia pasien saat kunjungan (setelah imputasi median). |
| `jenis_kelamin` | String | Jenis kelamin pasien (L/P). |
| `asuransi` | String | Jenis penjamin pembayaran (Umum / BPJS). |
| `status_pasien` | String | Status kedatangan (Baru / Lama). |
| `prioritas` | String | Tingkat kegawatdaruratan (Emergency / Non-Emergency). |
| `nama_poli` | String | Nama poliklinik tujuan layanan. |
| `nama_dokter` | String | Nama dokter yang menangani. |
| `kode_icd` | String | Kode standar internasional untuk klasifikasi penyakit. |
| `diagnosis` | String | Deskripsi medis mengenai penyakit pasien. |
| `waktu_kedatangan` | Datetime | Jam saat pasien tiba di rumah sakit. |
| `waktu_registrasi` | Datetime | Jam saat pasien selesai melakukan administrasi. |
| `waktu_mulai_layanan` | Datetime | Jam saat pasien mulai diperiksa oleh dokter. |
| `waktu_selesai_layanan`| Datetime | Jam saat pasien selesai mendapatkan layanan medis. |
| `durasi_layanan` | Integer | Total waktu pemeriksaan dokter (dalam menit). |
| `waktu_tunggu` | Integer | Total waktu dari registrasi hingga mulai dilayani (dalam menit). |
| `jumlah_antrian` | Integer | Jumlah orang yang sedang mengantre saat pasien datang. |
| `biaya` | Integer | Total biaya administrasi dan layanan (IDR). |
| `kepuasan_pasien` | Integer | Skor feedback pasien (Skala 1 - 5). |
| **Fitur Hasil Engineering** | | |
| `jam_kedatangan` | Integer | Ekstraksi jam dari waktu kedatangan (0-23). |
| `hari_kedatangan` | Integer | Indeks hari dalam seminggu (0=Senin, 6=Minggu). |
| `is_weekend` | Boolean | Penanda apakah kunjungan terjadi di akhir pekan (1) atau hari kerja (0). |
| `kategori_umur` | Category | Pengelompokkan umur (Anak, Remaja, Dewasa, Lansia). |
| `level_antrean` | Category | Klasifikasi kepadatan antrean (Rendah, Sedang, Tinggi). |
| `intensitas_biaya` | Float | Rasio biaya dibandingkan durasi layanan (Biaya / Menit). |