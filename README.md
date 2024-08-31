# Flask Student Grades Management System

Aplikasi web sederhana untuk mengelola data siswa, kelas, mata pelajaran, tugas, dan nilai siswa menggunakan Flask dan SQLAlchemy. Aplikasi ini menyediakan antarmuka CRUD (Create, Read, Update, Delete) untuk setiap entitas utama.

## Fitur

- **Kelola Siswa:** Tambah, lihat, edit, dan hapus data siswa.
- **Kelola Kelas:** Tambah, lihat, edit, dan hapus kelas.
- **Kelola Mata Pelajaran:** Tambah, lihat, edit, dan hapus mata pelajaran.
- **Kelola Tugas:** Tambah, lihat, edit, dan hapus tugas per kelas dan mata pelajaran.
- **Kelola Nilai:** Tambah, lihat, edit, dan hapus nilai tugas siswa.
- **Penanganan Error:** Halaman khusus untuk kesalahan 404 (Page Not Found) dan 500 (Internal Server Error).

## Teknologi yang Digunakan

- **Flask:** Framework web Python.
- **Flask-SQLAlchemy:** ORM untuk mengelola database.
- **SQLite:** Database untuk menyimpan data aplikasi.
- **HTML & CSS:** Antarmuka pengguna.
- **Bootstrap:** Untuk membuat tampilan lebih responsif dan menarik.

## Persyaratan

- Python 3.x
- Flask
- Flask-SQLAlchemy

## Instalasi

1. Clone repositori ini:

    ```bash
    git clone https://github.com/username/repo-name.git
    ```

2. Pindah ke direktori proyek:

    ```bash
    cd repo-name
    ```

3. Buat dan aktifkan virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Untuk Linux/macOS
    venv\Scripts\activate     # Untuk Windows
    ```

4. Instal dependensi:

    ```bash
    pip install -r requirements.txt
    ```

5. Buat database:

    ```bash
    flask shell
    >>> from app import db
    >>> db.create_all()
    ```

6. Jalankan aplikasi:

    ```bash
    flask run
    ```

7. Akses aplikasi di `http://127.0.0.1:5000/`.

## Struktur Proyek

```bash
|-- app.py                 # File utama aplikasi
|-- templates              # Direktori template HTML
|   |-- index.html
|   |-- students.html
|   |-- add_student.html
|   |-- update_student.html
|   |-- classes.html
|   |-- add_class.html
|   |-- update_class.html
|   |-- subjects.html
|   |-- add_subject.html
|   |-- update_subject.html
|   |-- assignments.html
|   |-- add_assignment.html
|   |-- update_assignment.html
|   |-- grades.html
|   |-- add_grade.html
|   |-- update_grade.html
|   |-- 404.html
|   |-- 500.html
|-- static                 # Direktori file statis (CSS, JS, gambar)
|-- requirements.txt       # Daftar dependensi
|-- README.md              # Dokumentasi proyek
```

## Penggunaan

1. **Menambahkan Siswa:** Akses `/students/add` untuk menambah siswa baru. Isi form dan pilih kelas yang sesuai.
2. **Mengelola Kelas:** Akses `/classes` untuk melihat daftar kelas, tambahkan, edit, atau hapus kelas sesuai kebutuhan.
3. **Mengelola Mata Pelajaran:** Akses `/subjects` untuk mengelola mata pelajaran.
4. **Mengelola Tugas:** Akses `/assignments` untuk menambah atau mengedit tugas per kelas dan mata pelajaran.
5. **Mengelola Nilai:** Akses `/grades` untuk menambahkan, melihat, atau mengedit nilai siswa.

## Penanganan Kesalahan

Aplikasi ini memiliki penanganan kesalahan untuk:
- **404 - Page Not Found:** Menampilkan halaman khusus ketika halaman tidak ditemukan.
- **500 - Internal Server Error:** Menampilkan halaman khusus ketika terjadi kesalahan server.

## Kontribusi

Kontribusi sangat diterima! Silakan buka pull request atau laporkan isu.

## Lisensi

Proyek ini dilisensikan di bawah lisensi MIT - lihat [LICENSE](LICENSE) untuk detail lebih lanjut.

