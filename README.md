# Polri Reimburse AI - Sistem Presisi

Sistem Reimbursement berbasis AI yang dirancang untuk personel Polri. Sistem ini mengintegrasikan deteksi OCR (Optical Character Recognition) untuk verifikasi otomatis kuitansi, manajemen dana lapangan, dan kontrol anggaran sistem oleh Admin Keuangan.

## Fitur Utama

- 🛡️ **Multi-Akses Presisi**: Login terpisah untuk Personel (Anggota) dan Admin Keuangan.
- 📸 **Verifikasi AI OCR**: Deteksi otomatis nominal kuitansi menggunakan OpenCV & Tesseract.
- 💼 **Dompet Lapangan Personel**: Kelola dana operasional mandiri di tangan personel.
- 📊 **Dashboard Otoritas**: Admin dapat memantau, menyetujui, atau menolak pengajuan secara real-time.
- 🎨 **UI Profesional**: Desain bersih, eye-friendly, dan responsif dengan tema Polri Blue.

## Teknologi

- **Backend**: FastAPI (Python), SQLAlchemy (PostgreSQL).
- **Frontend**: Vanilla JS, HTML5, CSS3 (Glassmorphism).
- **AI**: Pytesseract, OpenCV.

## Cara Instalasi

1. Clone Repository: `git clone https://github.com/firmandikarohman-web/app-reimburse/`
2. Setup Backend:
   - `cd backend`
   - `pip install -r requirements.txt`
   - Buat file `.env` (contoh di `.env.example`)
   - Jalankan: `uvicorn main:app --reload`
3. Setup Frontend:
   - Buka `frontend/index.html` langsung di browser atau lewat Live Server.

## Kontributor

- **Mabes Polri - Tim IT Presisi**

