CREATE DATABASE IF NOT EXISTS db_manajemen_siswa
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_manajemen_siswa;

CREATE TABLE IF NOT EXISTS users (
  username VARCHAR(50) PRIMARY KEY,
  password_hash VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS siswa (
  nis VARCHAR(30) PRIMARY KEY,
  nama VARCHAR(120) NOT NULL,
  kelas VARCHAR(40) NOT NULL,
  jurusan VARCHAR(80) NOT NULL,
  jk VARCHAR(5),
  telepon VARCHAR(30)
);
INSERT IGNORE INTO users(username,password_hash) VALUES ('admin','admin123');
INSERT IGNORE INTO siswa VALUES
('1001','Alya Putri','X RPL 1','RPL','P',''),
('1002','Rafi Pratama','X RPL 1','RPL','L',''),
('1003','Nadia Zahra','X TKJ 1','TKJ','P','');
