import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn=mysql.connector.connect(**DB_CONFIG)
        self.init()
    def run(self,sql,args=(),fetch=False):
        cur=self.conn.cursor()
        cur.execute(sql,args)
        result=cur.fetchall() if fetch else None
        cur.close()
        self.conn.commit()
        return result
    def init(self):
        self.run("""CREATE TABLE IF NOT EXISTS users(
          username VARCHAR(50) PRIMARY KEY,password_hash VARCHAR(255) NOT NULL)""")
        self.run("""CREATE TABLE IF NOT EXISTS siswa(
          nis VARCHAR(30) PRIMARY KEY,nama VARCHAR(120) NOT NULL,kelas VARCHAR(40) NOT NULL,
          jurusan VARCHAR(80) NOT NULL,jk VARCHAR(5),telepon VARCHAR(30))""")
        rows=self.run("SELECT username FROM users WHERE username=%s",("admin",),True)
        if not rows:self.run("INSERT INTO users(username,password_hash) VALUES(%s,%s)",("admin","admin123"))
        samples=[("1001","Alya Putri","X RPL 1","RPL","P",""),("1002","Rafi Pratama","X RPL 1","RPL","L",""),("1003","Nadia Zahra","X TKJ 1","TKJ","P","")]
        for r in samples:
            self.run("INSERT IGNORE INTO siswa VALUES(%s,%s,%s,%s,%s,%s)",r)
    def login(self,u,p):
        rows=self.run("SELECT password_hash FROM users WHERE username=%s",(u,),True)
        return bool(rows and rows[0][0]==p)
    def get_students(self,q="",kelas=None,jur=None):
        sql="SELECT nis,nama,kelas,jurusan,jk,telepon FROM siswa WHERE (nis LIKE %s OR nama LIKE %s)"
        args=[f"%{q}%",f"%{q}%"]
        if kelas:sql+=" AND kelas=%s";args.append(kelas)
        if jur:sql+=" AND jurusan=%s";args.append(jur)
        sql+=" ORDER BY nama"
        return self.run(sql,tuple(args),True)
    def stats(self):
        return {"total":self.run("SELECT COUNT(*) FROM siswa",fetch=True)[0][0],
                "kelas":self.run("SELECT COUNT(DISTINCT kelas) FROM siswa",fetch=True)[0][0],
                "jurusan":self.run("SELECT COUNT(DISTINCT jurusan) FROM siswa",fetch=True)[0][0]}
    def classes(self):return [r[0] for r in self.run("SELECT DISTINCT kelas FROM siswa ORDER BY kelas",fetch=True)]
    def majors(self):return [r[0] for r in self.run("SELECT DISTINCT jurusan FROM siswa ORDER BY jurusan",fetch=True)]
    def save(self,v,old=None):
        a=(v["NIS"],v["Nama"],v["Kelas"],v["Jurusan"],v["Jenis Kelamin"],v["Telepon"])
        if old:self.run("UPDATE siswa SET nis=%s,nama=%s,kelas=%s,jurusan=%s,jk=%s,telepon=%s WHERE nis=%s",a+(old,))
        else:self.run("INSERT INTO siswa VALUES(%s,%s,%s,%s,%s,%s)",a)
    def delete(self,n):self.run("DELETE FROM siswa WHERE nis=%s",(n,))
