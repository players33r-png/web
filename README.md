# Task Manager

Aplikasi **Task Manager** berbasis:

- HTML
- CSS
- Python standard library

Aplikasi berjalan di komputer sendiri melalui **server lokal Python**. Data task disimpan di file `tasks.json`, sehingga tidak membutuhkan database atau layanan online.

---

## 1. Struktur Project

Gunakan struktur folder berikut:

```text
task-manager-clean/
├── index.html
├── style.css
├── task_manager.py
├── README.md
└── tasks.json          # dibuat otomatis saat data disimpan
```

Tiga file utama aplikasi adalah:

```text
index.html       → tampilan dan interaksi halaman
style.css        → desain, layout, responsive, dan dark mode
task_manager.py  → server lokal, API, validasi, dan penyimpanan JSON
```

`tasks.json` tidak perlu dibuat secara manual. File tersebut akan dibuat otomatis ketika aplikasi menyimpan task.

---

## 2. Fitur

Versi ini menyediakan:

- Menambahkan task
- Mengedit task
- Menghapus task
- Menandai task selesai / belum selesai
- Prioritas:
  - Tinggi
  - Sedang
  - Rendah
- Kategori task
- Deadline dan waktu
- Catatan task
- Pencarian task
- Filter berdasarkan status
- Filter berdasarkan prioritas
- Filter berdasarkan kategori
- Sorting berdasarkan:
  - terbaru
  - terlama
  - deadline
  - prioritas
  - A-Z
  - Z-A
- Statistik:
  - total task
  - task selesai
  - task belum selesai
  - progress
- Penanda task yang sudah terlambat
- Menghapus semua task yang sudah selesai
- Dark mode
- Tampilan responsive untuk desktop dan mobile
- Penyimpanan otomatis ke `tasks.json`
- Validasi input pada sisi Python

---

## 3. Persyaratan

Minimal:

```text
Python 3.9+
Browser modern
```

Disarankan menggunakan:

```text
Python 3.10+
VS Code
Google Chrome / Microsoft Edge / Firefox
```

Tidak membutuhkan:

```text
Flask
Django
Node.js
npm
MySQL
XAMPP
pip install
Internet
```

Aplikasi hanya menggunakan **Python Standard Library**.

---

## 4. Cara Menjalankan di VS Code

### Langkah 1 — Buka folder

Buka folder project:

```text
task-manager-clean
```

di VS Code.

### Langkah 2 — Buka Terminal

Di VS Code pilih:

```text
Terminal → New Terminal
```

### Langkah 3 — Jalankan Python

Windows:

```bash
python task_manager.py
```

Jika perintah `python` tidak tersedia, coba:

```bash
py task_manager.py
```

Linux / macOS:

```bash
python3 task_manager.py
```

### Langkah 4 — Buka browser

Program akan mencoba membuka browser secara otomatis.

Jika tidak terbuka, buka:

```text
http://127.0.0.1:8000
```

atau:

```text
http://localhost:8000
```

---

## 5. Penting: Jangan Membuka `index.html` Langsung

Jangan menjalankan:

```text
index.html
```

dengan double-click jika ingin menggunakan fitur penyimpanan dan API.

Gunakan:

```bash
python task_manager.py
```

Karena `task_manager.py` bertindak sebagai server lokal yang menghubungkan:

```text
Browser
   ↓
index.html
   ↓
JavaScript / fetch()
   ↓
Python API
   ↓
tasks.json
```

---

## 6. Cara Menghentikan Aplikasi

Kembali ke terminal tempat Python berjalan, lalu tekan:

```text
Ctrl + C
```

Server akan berhenti.

Data yang sudah tersimpan di `tasks.json` tetap ada.

---

## 7. Penyimpanan Data

Data disimpan dalam:

```text
tasks.json
```

Contoh struktur sederhananya:

```json
[
  {
    "id": 1,
    "title": "Belajar Python",
    "category": "Belajar",
    "priority": "Tinggi",
    "deadline": "2026-10-10",
    "time": "19:00",
    "notes": "Mempelajari dasar Python",
    "completed": false
  }
]
```

File ini adalah database sederhana berbasis JSON.

Karena file berada di folder project, data tetap tersedia setelah aplikasi ditutup dan dijalankan kembali.

---

## 8. Reset Semua Data

Jika ingin menghapus seluruh task:

1. Hentikan server Python dengan `Ctrl + C`.
2. Hapus:

```text
tasks.json
```

3. Jalankan kembali:

```bash
python task_manager.py
```

Aplikasi akan membuat data baru saat task berikutnya disimpan.

---

## 9. API Lokal

`task_manager.py` menyediakan API sederhana.

| Method | Endpoint | Fungsi |
|---|---|---|
| GET | `/api/tasks` | Mengambil seluruh task |
| POST | `/api/tasks` | Membuat task baru |
| PUT | `/api/tasks/{id}` | Mengubah task |
| POST | `/api/tasks/{id}/toggle` | Mengubah status task |
| DELETE | `/api/tasks/{id}` | Menghapus satu task |
| DELETE | `/api/tasks/completed` | Menghapus seluruh task yang selesai |

API tersebut digunakan oleh JavaScript di `index.html`.

---

## 10. Jika Port 8000 Digunakan Program Lain

Jika muncul error seperti:

```text
Address already in use
```

berarti port `8000` sedang digunakan.

Buka:

```text
task_manager.py
```

Cari:

```python
PORT = 8000
```

ubah menjadi misalnya:

```python
PORT = 8080
```

Kemudian jalankan:

```bash
python task_manager.py
```

Buka:

```text
http://127.0.0.1:8080
```

---

## 11. Jika `python` Tidak Dikenali

Jika muncul:

```text
'python' is not recognized
```

coba:

```bash
py task_manager.py
```

Jika tetap tidak bisa, Python kemungkinan belum terpasang atau belum masuk ke PATH.

Pastikan Python dapat dipanggil dengan:

```bash
python --version
```

atau:

```bash
py --version
```

---

## 12. Jika VS Code Menampilkan Banyak Error Pylance

Versi `task_manager.py` ini dibuat ulang dengan struktur Python yang lebih sederhana dan konsisten untuk menghindari error seperti:

```text
Expected expression to the right of "="
Unexpected indentation
```

Jika VS Code masih menampilkan error dari file lama:

1. Pastikan file yang dibuka adalah:

```text
task_manager.py
```

dari folder project yang baru.
2. Pastikan tidak ada potongan kode lama yang tercampur.
3. Simpan file dengan `Ctrl + S`.
4. Pastikan VS Code menggunakan interpreter Python yang benar.
5. Restart VS Code jika daftar diagnostic belum diperbarui.

Untuk memeriksa syntax Python dari terminal, jalankan:

```bash
python -m py_compile task_manager.py
```

Jika tidak menghasilkan pesan error, syntax Python berhasil diperiksa.

---

## 13. Alur Program

Secara sederhana, aplikasi bekerja seperti ini:

```text
┌─────────────────────┐
│      Browser        │
│   index.html        │
└─────────┬───────────┘
          │
          │ HTTP / fetch()
          ▼
┌─────────────────────┐
│   task_manager.py   │
│    Local Server     │
└─────────┬───────────┘
          │
          │ read / write
          ▼
┌─────────────────────┐
│      tasks.json     │
│   Penyimpanan Data  │
└─────────────────────┘
```

### `index.html`

Berisi:

- struktur halaman
- form task
- daftar task
- statistik
- filter
- pencarian
- JavaScript untuk interaksi

### `style.css`

Mengatur:

- layout
- warna
- tombol
- card
- form
- responsive design
- dark mode
- tampilan mobile

### `task_manager.py`

Menangani:

- server HTTP lokal
- API task
- validasi input
- membaca `tasks.json`
- menulis `tasks.json`
- membuat ID task
- update task
- delete task

---

## 14. Keamanan dan Batasan

Aplikasi ini ditujukan untuk penggunaan **lokal / pribadi**.

Server menggunakan:

```text
127.0.0.1
```

Artinya server hanya diakses dari komputer yang menjalankannya.

Aplikasi tidak menggunakan:

- akun pengguna
- autentikasi
- database server
- cloud storage
- API eksternal

Karena itu, jangan menjadikan aplikasi ini sebagai server publik tanpa menambahkan sistem keamanan yang sesuai.

---

## 15. Backup Data

Untuk melakukan backup task, cukup salin file:

```text
tasks.json
```

ke lokasi lain.

Untuk mengembalikan data:

1. Tutup aplikasi.
2. Letakkan kembali `tasks.json` ke folder project.
3. Jalankan:

```bash
python task_manager.py
```

---

## 16. Checklist Menjalankan Project

Gunakan checklist berikut:

```text
[ ] Python sudah terpasang
[ ] Folder project dibuka di VS Code
[ ] index.html tersedia
[ ] style.css tersedia
[ ] task_manager.py tersedia
[ ] Tidak ada file Python lama yang tercampur
[ ] Jalankan python task_manager.py
[ ] Buka http://127.0.0.1:8000
```

---

## 17. Perintah Utama

### Menjalankan aplikasi

Windows:

```bash
python task_manager.py
```

atau:

```bash
py task_manager.py
```

Linux/macOS:

```bash
python3 task_manager.py
```

### Mengecek syntax Python

```bash
python -m py_compile task_manager.py
```

### Menghentikan server

```text
Ctrl + C
```

---

## 18. Catatan Versi

Versi ini dibuat ulang dari awal dengan tujuan utama:

- menghilangkan error syntax Python
- memperbaiki masalah indentasi
- memisahkan frontend dan backend dengan jelas
- menggunakan Python Standard Library
- membuat penyimpanan lokal menggunakan JSON
- membuat aplikasi tetap mudah dijalankan dari VS Code
- mempertahankan struktur sederhana: HTML + CSS + Python

File utama yang diperlukan hanya:

```text
index.html
style.css
task_manager.py
```

Sedangkan:

```text
README.md
```

digunakan sebagai dokumentasi dan:

```text
tasks.json
```

dibuat otomatis sebagai penyimpanan data.
