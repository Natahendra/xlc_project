````markdown
# FastAPI Project – API Backend

Project ini adalah API backend yang dibangun menggunakan:

- **FastAPI** – Web framework
- **SQLModel** – ORM (berbasis SQLAlchemy + Pydantic)
- **Alembic** – Database migration
- **Uvicorn** – ASGI server

README ini ditujukan untuk **developer baru** yang ingin melakukan **clone project dan menjalankannya dari nol** hingga mendapatkan **database yang sama** dengan developer awal.

---

## Daftar Isi

- [Prerequisites](#prerequisites)
- [Clone Repository](#clone-repository)
- [Struktur Project](#struktur-project)
- [Setup Virtual Environment](#setup-virtual-environment)
- [Install Dependencies](#install-dependencies)
- [Konfigurasi Environment Variable](#konfigurasi-environment-variable)
- [Setup Database](#setup-database)
- [Menjalankan Migration](#menjalankan-migration)
- [Menjalankan Aplikasi](#menjalankan-aplikasi)
- [Akses API & Dokumentasi](#akses-api--dokumentasi)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Pastikan software berikut sudah ter-install di komputer kamu:

- **Python 3.10 atau lebih baru**
  ```bash
  python --version
  ```
````

- **pip** (biasanya sudah include dengan Python)

- **Git**

  ```bash
  git --version
  ```

- **Database Server**

  - MySQL / SQLite (jika project menggunakan ini)
  - PostgreSQL (disarankan)

---

## Clone Repository

Clone repository ke local machine:

```bash
git clone https://github.com/abibinyun/xlc-rewrite.git
cd xlc-rewrite
```

---

## Struktur Project

Contoh struktur folder utama:

```text
.
├── env/
├── alembic/
│   ├── versions/
│   └── env.py
├── lib/
│   └── database.py
├── models/
├── repositories/
├── routers/
├── schemas/
├── services/
├── alembic.ini
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup Virtual Environment

Disarankan **SELALU** menggunakan virtual environment.

### Buat Virtual Environment

```bash
python -m venv venv
```

### Aktifkan Virtual Environment

#### Windows (PowerShell)

```bash
venv\Scripts\activate
```

#### macOS / Linux

```bash
source venv/bin/activate
```

Jika berhasil, prompt terminal akan berubah menjadi:

```text
(venv)
```

---

## Install Dependencies

Install semua dependency Python:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Pastikan tidak ada error saat instalasi.

---

## Konfigurasi Environment Variable

Project ini menggunakan environment variable.

### 1. Copy file `.env.example`

```bash
cp .env.example .env
```

### 2. Edit file `.env`

Sesuaikan dengan konfigurasi database lokal kamu:

```env
APP_ENV=development
APP_NAME=fastapi-api

DATABASE_URL=mysql+pymysql://root:@localhost:3306/db_name(xlc_rewrite)

SECRET_KEY=super-secret-key
```

> ⚠️ **PENTING**
> Pastikan database (`db_name`) sudah dibuat di database server.

---

## Setup Database

### MySQL (contoh)

#### 1️⃣ Masuk ke MySQL via terminal

```bash
mysql -u root -p
```

> `-u root` → username MySQL
> `-p` → nanti akan diminta password

#### 2️⃣ Buat database baru

```sql
CREATE DATABASE xlc_rewrite;
```

> Ganti `xlc_rewrite` dengan nama database yang kamu inginkan.

#### 3️⃣ Buat user (opsional tapi disarankan)

```sql
CREATE USER 'xlc_user'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON xlc_rewrite.* TO 'xlc_user'@'localhost';
FLUSH PRIVILEGES;
```

> Ganti `xlc_user` dan `password123` sesuai kebutuhan.

#### 4️⃣ Keluar dari MySQL

```sql
EXIT;
```

---

### phpMyAdmin (opsional, GUI)

1. Login ke **phpMyAdmin** (biasanya `http://localhost/phpmyadmin`)
2. Klik **Databases** → **Create Database**
3. Masukkan nama database (`xlc_rewrite`) → klik **Create**
4. (Opsional) Tambahkan user baru → beri **all privileges** ke database tersebut

---

### 5️⃣ Update `.env`

```env
# Contoh MySQL
DATABASE_URL=mysql+pymysql://xlc_user:password123@localhost:3306/xlc_rewrite
```

- Sesuaikan username, password, host, port, dan database
- Ini akan dipakai **SQLModel + Alembic** otomatis

---

## Menjalankan Migration

Project ini menggunakan **Alembic** dan migration **SUDAH TERSEDIA**.

### Pastikan Alembic Mengarah ke Database yang Benar

Cek file `alembic.ini` dan `env.py`:

- `sqlalchemy.url` **menggunakan DATABASE_URL dari `.env`**

Biasanya sudah otomatis jika project dikonfigurasi dengan benar.

---

### Jalankan Migration

```bash
alembic upgrade head
```

Jika berhasil, maka:

- Semua tabel akan dibuat
- Struktur database akan **sama persis** dengan developer awal

Untuk mengecek status migration:

```bash
alembic current
```

---

## Menjalankan Aplikasi

Jalankan FastAPI menggunakan Uvicorn:

```bash
uvicorn app.main:app --reload
```

Jika berhasil, kamu akan melihat output seperti:

```text
Uvicorn running on http://127.0.0.1:8000
```

---

## Akses API & Dokumentasi

FastAPI menyediakan dokumentasi otomatis:

- **Swagger UI**

  ```
  http://127.0.0.1:8000/docs
  ```

- **ReDoc**

  ```
  http://127.0.0.1:8000/redoc
  ```

---

## Troubleshooting

### ❌ Error: `ModuleNotFoundError`

Pastikan:

- Virtual environment aktif
- Dependency sudah di-install

```bash
pip list
```

---

### ❌ Error koneksi database

Periksa:

- Database server sedang berjalan
- `DATABASE_URL` di `.env`
- Username & password database benar

---

### ❌ Alembic error saat upgrade

Coba:

```bash
alembic downgrade base
alembic upgrade head
```

> ⚠️ Hanya aman dilakukan di **development**, jangan di production.

---

## Catatan Tambahan

- Jangan commit file `.env`
- Selalu jalankan migration setelah `git pull`
- Gunakan virtual environment untuk setiap project

---

## License

MIT License (atau sesuai kebutuhan project)
