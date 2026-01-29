## Bridge_Database_EDS_Manufacture – Backend API

Backend ini adalah layanan API berbasis **FastAPI** yang mengakses database **MySQL/MariaDB** dan dapat digunakan oleh aplikasi Flutter, Postman, atau klien HTTP lainnya.

- **Bahasa**: Python
- **Framework**: FastAPI
- **Database utama saat ini**: `qa` di server `10.62.144.231`
- **Driver DB**: mysql-connector-python

---

## Persiapan & Instalasi

- Pastikan sudah berada di folder project:

```bash
cd C:\laragon\www\Bridge_Database_EDS_Manufacture
```

- Install dependency:

```bash
pip install -r requirements.txt
```

> Gunakan interpreter Python yang sama seperti yang dipakai untuk menjalankan server (cek dengan `python --version` dan `where python` jika perlu).

---

## Menjalankan Server

Jalankan perintah berikut dari folder project:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

- Server akan berjalan di: `http://IP_SERVER:8000`
- Dokumentasi Swagger tersedia di: `http://IP_SERVER:8000/api/docs`
- Dokumentasi Redoc tersedia di: `http://IP_SERVER:8000/api/redoc`

Contoh:

- Dari mesin lokal: `http://localhost:8000/api/docs`
- Dari perangkat lain di jaringan: `http://192.168.151.232:8000/api/docs`

---

## Konfigurasi Database (Ringkasan)

Konfigurasi database dikelola di file `app/config.py`.

- **Server DB QA saat ini**:
  - **Host**: `10.62.144.231`
  - **Port**: `3306`
  - **User**: `root`
  - **Password**: `beny1234`
  - **Database**: `qa`

Jika nanti environment berubah (host, user, password, nama database), cukup update nilai di `app/config.py`.

---

## Menjalankan dengan Docker (Port 2026)

Backend ini bisa dijalankan via Docker dan akan expose API ke **port `2026`** pada host.

### Prasyarat

- Docker Desktop sudah terinstall dan berjalan.

### Jalankan

Di folder project:

```bash
docker compose up --build -d
```

Setelah itu API bisa diakses di:

- `http://localhost:2026/api/docs`
- `http://localhost:2026/api/v1/health`
- `http://localhost:2026/api/v1/qa/tables`

### Mengubah konfigurasi DB (Docker)

Edit file `docker-compose.yml` pada bagian `environment`:

- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

Lalu restart container:

```bash
docker compose up --build -d
```

### Stop

```bash
docker compose down
```

---

## Endpoint yang Tersedia

Semua contoh di bawah menggunakan base URL:

```text
http://IP_SERVER:8000
```

Ganti `IP_SERVER` dengan:

- `localhost` jika akses dari mesin yang sama, atau
- IP LAN seperti `192.168.151.232` jika diakses dari perangkat lain.

---

### 1. Health Check

- **Method**: `GET`
- **URL**: `/api/v1/health`
- **Deskripsi**: Mengecek apakah backend berjalan dengan normal.

**Contoh request (Postman / browser):**

```text
GET http://IP_SERVER:8000/api/v1/health
```

**Contoh response:**

```json
{
  "status": "ok",
  "message": "Cyber Backend API is running"
}
```

---

### 2. QA Database – Daftar Tabel

- **Method**: `GET`
- **URL**: `/api/v1/qa/tables`
- **Deskripsi**: Mengambil daftar semua nama tabel yang ada di database `qa`.

**Contoh request:**

```text
GET http://IP_SERVER:8000/api/v1/qa/tables
```

**Contoh response:**

```json
{
  "status": "success",
  "message": "Tables fetched successfully",
  "data": [
    "barcode_qa",
    "barcode_qa_backup",
    "chopper"
  ]
}
```

Informasi ini berguna untuk mengetahui tabel apa saja yang tersedia sebelum melakukan query data.

---

### 3. QA Database – Ambil Data dari Tabel Tertentu

- **Method**: `GET`
- **URL**: `/api/v1/qa/{nama_tabel}`
- **Query parameter**:
  - **`limit`** *(opsional)*: jumlah maksimum baris yang dikembalikan.
    - Default: `100`
    - Minimum: `1`
    - Maksimum: `1000`
- **Deskripsi**: Mengambil data dari tabel tertentu di database `qa`.

**Aturan nama tabel (`{nama_tabel}`):**

- Hanya boleh berisi **huruf**, **angka**, dan **underscore**: `[A-Za-z0-9_]+`
- Contoh nama tabel valid: `barcode_qa`, `barcode_qa_backup`, `chopper`, dll.

#### Contoh 3.1 – Ambil semua data default (limit 100)

```text
GET http://IP_SERVER:8000/api/v1/qa/barcode_qa
```

**Contoh response:**

```json
{
  "status": "success",
  "message": "Data fetched from table 'barcode_qa'",
  "data": [
    {
      "id": 5,
      "nama_barang": "LUMP",
      "lokasi": "EXT 1"
    },
    {
      "id": 6,
      "nama_barang": "JOINT",
      "lokasi": "EXT 1"
    }
  ]
}
```

#### Contoh 3.2 – Batasi jumlah baris

```text
GET http://IP_SERVER:8000/api/v1/qa/chopper?limit=50
```

**Keterangan:**

- `limit=50` → hanya mengembalikan 50 baris pertama dari tabel `chopper`.
- Berguna untuk menghindari response terlalu besar.

#### Kemungkinan error

- **400 Bad Request**: jika `nama_tabel` mengandung karakter tidak diizinkan.
- **500 Internal Server Error**: jika tabel tidak ada, database tidak bisa diakses, atau terjadi error internal lain.

---

### 4. Endpoint Users (Opsional / Contoh)

Terdapat juga router `users` yang mengambil data dari tabel `users` (jika database dan tabel tersebut dikonfigurasi dan tersedia).

- **Method**: `GET`
- **URL**: `/api/v1/users`
- **Deskripsi**: Mengambil semua data dari tabel `users`.

Endpoint ini awalnya dibuat sebagai contoh, dan bisa disesuaikan atau dihapus jika tidak diperlukan.

---

## Cara Pakai Singkat (Postman)

1. Pastikan server sudah berjalan:

   ```bash
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Buka Postman dan set **Base URL**:

   ```text
   http://IP_SERVER:8000
   ```

3. Coba beberapa request:

   - Cek health:

     ```text
     GET http://IP_SERVER:8000/api/v1/health
     ```

   - Lihat semua tabel di `qa`:

     ```text
     GET http://IP_SERVER:8000/api/v1/qa/tables
     ```

   - Ambil data dari tabel `barcode_qa`:

     ```text
     GET http://IP_SERVER:8000/api/v1/qa/barcode_qa
     ```

   - Ambil data dari tabel `chopper` dengan limit 50 baris:

     ```text
     GET http://IP_SERVER:8000/api/v1/qa/chopper?limit=50
     ```

---

## Cara Pakai Singkat (Flutter)

Contoh sangat sederhana menggunakan package `http`:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

Future<void> fetchBarcodeQa() async {
  final uri = Uri.parse('http://IP_SERVER:8000/api/v1/qa/barcode_qa');
  final response = await http.get(uri);

  if (response.statusCode == 200) {
    final jsonBody = jsonDecode(response.body);
    final data = jsonBody['data']; // list row dari tabel barcode_qa
    // TODO: mapping ke model Dart sesuai kebutuhan
  } else {
    // TODO: handle error
  }
}
```

Ganti `IP_SERVER` dengan IP backend yang sebenarnya (misalnya `192.168.151.232` atau `103.236.140.19` jika backend dipindahkan ke server tersebut).

---

## Catatan Penting

- Pastikan jaringan mengizinkan koneksi dari backend ke database (`10.62.144.231:3306`).
- Untuk produksi, sebaiknya:
  - Tidak menggunakan user `root` langsung.
  - Password dan konfigurasi database dipindah ke **environment variable** atau file `.env`, bukan hard-coded.
  - Mengatur `allow_origins` pada CORS agar tidak `*` (batasi hanya domain aplikasi).

