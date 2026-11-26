APLIKASI SIMS - MANAJEMEN DATA SISWA (MYSQL)

PERSIAPAN MYSQL XAMPP
1. Buka XAMPP Control Panel.
2. Klik Start pada Apache dan MySQL.
3. Buka http://localhost/phpmyadmin
4. Pilih tab Import, pilih file database_mysql.sql dari folder aplikasi, lalu klik Import/Go.
   File SQL membuat database db_manajemen_siswa beserta tabel dan data contoh.
5. Jika MySQL memakai password root, edit config.py dan isi nilai password.

MENJALANKAN APLIKASI
1. Buka folder ini di VS Code.
2. Terminal: py -m pip install -r requirements.txt
3. Jalankan: py main.py

LOGIN AWAL: admin / admin123

FITUR
Login, dashboard statistik siswa/kelas/jurusan, tambah/edit/hapus siswa,
pencarian NIS/nama, filter kelas/jurusan, ekspor Excel XLSX, dan ekspor PDF.

CATATAN: Aplikasi memakai MySQL XAMPP. MySQL harus aktif dan database sudah di-import.
Jika koneksi gagal, cek host, port, username, password pada config.py.
