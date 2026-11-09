# LibrisQuest — Gamified Digital Reading Ecosystem

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python)](https://python.org/)
[![Database](https://img.shields.io/badge/Database-MySQL-4479A1?style=flat&logo=mysql)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**LibrisQuest** adalah ekosistem membaca materi akademik berbasis gamifikasi terpadu (*gamified digital reader*) yang dirancang untuk membantu mahasiswa dan pelajar membangun kebiasaan membaca konsisten, mengatasi kejenuhan materi tebal, serta mengubah rutinitas belajar pasif menjadi petualangan akademik yang terukur dan kompetitif.

Proyek ini dirancang menggunakan pendekatan bertahap berbasis riset validasi lapangan (*Lean Startup*), perancangan arsitektur berstandar industri, serta implementasi *monorepo* modern.

---

## Daftar Isi
- [1. Ringkasan Eksekutif & UVP Produk](#1-ringkasan-eksekutif--uvp-produk)
- [2. Hasil Riset & Validasi Lapangan](#2-hasil-riset--validasi-lapangan)
  - [A. Javelin Board (Lean Startup Experiment)](#a-javelin-board-lean-startup-experiment)
  - [B. Benchmark Desain (Design Sprint — Lightning Demos)](#b-benchmark-desain-design-sprint--lightning-demos)
- [3. Cakupan 8 Fitur Utama](#3-cakupan-8-fitur-utama)
- [4. Arsitektur Teknis & Standar Monorepo](#4-arsitektur-teknis--standar-monorepo)
- [5. Panduan Menjalankan Proyek (Getting Started)](#5-panduan-menjalankan-proyek-getting-started)
- [6. Standar Commit & Konvensi Rekayasa](#6-standar-commit--konvensi-rekayasa)

---

## 1. Ringkasan Eksekutif & UVP Produk

* **Nama Produk:** LibrisQuest
* **Target Pengguna:** Mahasiswa aktif jenjang sarjana (khususnya semester 1–4) dan pelajar jenjang SMA/SMK dengan beban bacaan buku teks, modul perkuliahan, atau jurnal ilmiah yang tebal.
* **Permasalahan Utama (Tervalidasi):** Mahasiswa mengalami kesulitan mempertahankan fokus, disiplin, dan konsistensi ketika membaca referensi kuliah di gawai. Hal ini dipicu oleh ketiadaan timbal balik instan (*instant gratification*) serta tingginya godaan distraksi media sosial (TikTok, Instagram, YouTube Shorts).
* **Solusi Inti:** Mengintegrasikan mesin pembaca digital (*digital reader*) dengan sistem gamifikasi terpadu: pelacak kemajuan visual real-time, hadiah mikro instan (XP dan streak harian), evaluasi pemahaman format santai (mini-kuis trivia), serta papan peringkat sosial berkala (*weekly cohort league*).

### Rumusan UVP Message (Resmi):
> "Produk kami **LibrisQuest** membantu **mahasiswa (khususnya semester 1–4)** yang **sedang mencari referensi kuliah dan ingin membangun rutinitas membaca konsisten** dengan mengurangi **rasa malas, kejenuhan, dan distraksi media sosial saat membaca materi perkuliahan yang tebal**, dan mencapai **pengalaman membaca yang seru, terukur, dan kompetitif melalui ekosistem gamifikasi terpadu (pelacak progres visual, mini-kuis pemahaman berhadiah XP & streak, serta papan peringkat sosial antarmahasiswa)**, berbeda dengan **perpustakaan digital atau aplikasi e-reader konvensional** yang **hanya sekadar menyediakan koleksi buku pasif tanpa elemen evaluasi interaktif maupun pendorong motivasi sosial**."

---

## 2. Hasil Riset & Validasi Lapangan

Pengembangan LibrisQuest berakar pada riset empiris dan validasi langsung ke target pengguna menggunakan metodologi *Lean Startup* dan *Design Sprint*.

### A. Javelin Board (Lean Startup Experiment)

* **Metode:** *Semi-Structured Customer Interview* (1-on-1, durasi 15–20 menit) menggunakan Skenario Konsep terhadap 5 mahasiswa aktif di wilayah perguruan tinggi Bandung Raya.
* **Hasil Validasi:** **5 dari 5 Responden Valid (Tingkat Validasi 100%)**.
* **Keputusan Bisnis:** **PERSEVERE** — Hipotesis masalah dan konsep solusi terbukti valid; perancangan dilanjutkan ke fase rekayasa teknis.
* **Temuan Kunci (*Learnings*):**
  1. **Daily Streak adalah Pemicu Psikologis Terkuat:** Mahasiswa terdorong oleh efek *loss aversion* (takut kehilangan rekor hari), sehingga rela meluangkan waktu minimal 10 menit setiap hari untuk mempertahankan status streak.
  2. **Format Mini-Kuis Harus Bersifat Trivia Cepat:** Mini-kuis harus selesai dalam <1 menit (maksimal 3 soal pilihan ganda berhadiah bonus XP). Format esai atau analisis panjang dihindari karena menimbulkan beban psikologis baru layaknya tugas kuliah formal.
  3. **Kebutuhan Bring Your Own Book (BYOB):** Mahasiswa tidak hanya menginginkan pustaka umum, melainkan sangat membutuhkan fitur unggah modul atau slide materi PDF dari dosen mereka sendiri untuk dibaca dan digamifikasi di dalam aplikasi.

### B. Benchmark Desain (Design Sprint — Lightning Demos)

1. **Duolingo:** Mengadopsi pola psikologi *Daily Streak*, perolehan XP instan per halaman yang dibaca, animasi *level-up / badge*, dan *leaderboard* liga mingguan 30 orang per kelompok (bukan ranking global tanpa akhir) agar kompetisi terasa dapat dicapai.
2. **Knowt:** Mengadopsi pola *drag-and-drop* instan dokumen akademik serta ekstraksi poin-poin kunci materi kuliah ke kartu belajar.
3. **The StoryGraph / Basmo:** Mengadopsi bilah progres membaca (*reading progress bar*) dinamis di dasar layar dengan persentase real-time dan kartu rekap pencapaian harian.
4. **Quizizz:** Meniru atmosfer kuis ceria berbasis game trivia yang interaktif tanpa ketegangan suasana ujian.
5. **NotebookLM:** Pemecahan otomatis dokumen tebal menjadi struktur bab tematik, yang dalam LibrisQuest ditransformasikan menjadi rute misi belajar (*Quest Map*).

---

## 3. Cakupan 8 Fitur Utama

LibrisQuest dibangun di atas 8 pilar fitur utama:

| No | Fitur | Deskripsi Fungsional |
|---|---|---|
| 1 | **Bring Your Own Book (BYOB) Upload** | Unggah modul kuliah, slide kuliah, atau e-book PDF mandiri dari dosen dengan ekstraksi metadata otomatis. |
| 2 | **Visual Reading Progress Tracker** | Indikator progres visual (*progress bar*) dan persentase kemajuan membaca halaman demi halaman secara *real-time*. |
| 3 | **Instant XP (Experience Points) Engine** | Akumulasi XP secara instan per halaman bacaan yang diselesaikan untuk memberikan *instant feedback*. |
| 4 | **Daily Streak & Habit Loop** | Penghitung hari membaca berturut-turut dengan toleransi zona waktu untuk menjaga retensi dan memutus prokrastinasi. |
| 5 | **Dynamic Level & Achievement Badges** | Progresi level pengguna dan lencana pencapaian berdasarkan milestone XP, bab, dan konsistensi membaca. |
| 6 | **Cohort Weekly Leaderboard** | Papan peringkat mingguan berbasis kohort liga (30 pengguna per divisi) antarteman atau rekan kampus. |
| 7 | **Interactive Chapter Mini-Quiz** | Evaluasi pemahaman instan (3–5 soal trivia pilihan ganda) setelah menyelesaikan bab dengan *reward* bonus XP besar. |
| 8 | **Automated Content Summary** | Ekstraksi ringkasan poin-poin penting materi bab secara otomatis untuk mempermudah *quick review* sebelum ujian. |

---

## 4. Arsitektur Teknis & Standar Monorepo

Repositori ini menerapkan pola **Monorepo** pada branch `main` guna menyatukan backend API dan frontend client dalam satu ekosistem terpadu.

```
LibrisQuest/
├── .gitignore               # Konfigurasi pengabaian file Git monorepo
├── README.md                # Dokumentasi spesifikasi produk & panduan teknis
├── backend/                 # Layanan REST API (FastAPI)
│   ├── .env.example         # Templat variabel lingkungan backend
│   ├── Dockerfile.example   # Konfigurasi container backend
│   ├── docker-compose.yaml.example
│   ├── requirements.txt     # Dependensi Python
│   ├── app/
│   │   ├── api/
│   │   │   ├── dependencies/# Injeksi dependensi (repositories & services)
│   │   │   └── routes/      # Definisi router & endpoint API
│   │   ├── core/            # Konfigurasi, koneksi database, limiter, logger
│   │   ├── dto/             # Data Transfer Objects (Pydantic schemas)
│   │   ├── enums/           # Konstanta enum sistem
│   │   ├── integrations/    # Integrasi pihak ketiga (Telegram, AI service)
│   │   ├── middlewares/     # JWT authentication, CORS, rate limiting
│   │   ├── models/          # Entitas data domain
│   │   ├── repositories/    # Abstraksi akses data & query SQL
│   │   ├── services/        # Logika bisnis inti (XP, streak, auth, kuis)
│   │   ├── utils/           # Helper fungsi, hashing, serialisasi
│   │   └── main.py          # Entry point aplikasi FastAPI
│   └── deployments/         # Skrip otomasi deployment & reverse proxy
└── frontend/                # Client aplikasi web/mobile (Tahap Selanjutnya)
```

### Komponen Backend:
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12+) — framework asinkron berkinerja tinggi dengan validasi tipe data berbasis Pydantic.
* **Database:** **MySQL** — penyimpanan relasional untuk data pengguna, dokumen, sesi baca, log XP, status streak, dan skor kuis.
* **Keamanan:** Autentikasi stateless menggunakan JWT (JSON Web Tokens), enkripsi kata sandi dengan Bcrypt, perlindungan CORS terkonfigurasi, serta pembatasan laju request (*Rate Limiting*) via SlowAPI.

---

## 5. Panduan Menjalankan Proyek (Getting Started)

### Prasyarat
* Python 3.12 atau versi lebih baru
* MySQL Server 8.0+
* Git

### Langkah Instalasi Backend

1. **Masuk ke direktori backend:**
   ```bash
   cd backend
   ```

2. **Buat dan aktifkan lingkungan virtual (virtual environment):**
   * Di Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   * Di Linux / macOS:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Pasang paket dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Konfigurasi Variabel Lingkungan:**
   Salin file templat konfigurasi dan sesuaikan kredensial MySQL lokal Anda:
   ```bash
   cp .env.example .env
   ```

5. **Jalankan Server Pengembangan:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

6. **Akses Dokumentasi API Interaktif:**
   * **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
   * **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)
   * **Health Check Endpoint:** [http://localhost:8000/](http://localhost:8000/)

---

## 6. Standar Commit & Konvensi Rekayasa

Setiap perubahan kode dalam repositori ini mematuhi standar [Conventional Commits](https://www.conventionalcommits.org/):
* `feat:` Penambahan fitur baru (misal: endpoint baru, migrasi database, kalkulasi XP).
* `fix:` Perbaikan bug atau kesalahan logika.
* `docs:` Pembaruan atau penambahan dokumentasi proyek.
* `chore:` Pemeliharaan dependensi, konfigurasi build, atau inisialisasi berkas.
* `refactor:` Restrukturisasi kode tanpa mengubah fungsionalitas eksternal.
* `test:` Penambahan atau pembaruan unit/integration test.
