import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import Database
from exports import export_excel, export_pdf

BG="#eef4fb"; PANEL="#ffffff"; BLUE="#2563eb"; DARK="#17345f"; MUTED="#64748b"
GREEN="#16a34a"; RED="#dc2626"; GOLD="#d97706"

class App:
    def __init__(self,root):
        self.root=root; root.title("SIMS - Manajemen Data Siswa"); root.geometry("1180x750");root.minsize(980,620)
        try:self.db=Database()
        except Exception as e:
            messagebox.showerror("Koneksi MySQL gagal",f"Tidak bisa terhubung ke MySQL.\n\n{e}\n\nPeriksa XAMPP, database, dan config.py.")
            root.destroy();return
        self.user=None
        st=ttk.Style(); st.theme_use("clam")
        st.configure("Treeview",background="white",foreground=DARK,fieldbackground="white",rowheight=32,font=("Segoe UI",9))
        st.configure("Treeview.Heading",background="#dbeafe",foreground=DARK,font=("Segoe UI",9,"bold"))
        st.map("Treeview",background=[("selected","#bfdbfe")])
        self.login()
    def clear(self):
        for w in self.root.winfo_children():w.destroy()
    def btn(self,p,t,c,col=BLUE):
        return tk.Button(p,text=t,command=c,bg=col,fg="white",activebackground=col,relief="flat",cursor="hand2",font=("Segoe UI",9,"bold"),padx=12,pady=8)
    def ent(self,p):
        return tk.Entry(p,bg="white",fg=DARK,insertbackground=DARK,relief="flat",font=("Segoe UI",10),highlightthickness=1,highlightbackground="#cbd5e1")
    def login(self):
        self.clear();self.root.configure(bg=BG)
        card=tk.Frame(self.root,bg=PANEL,padx=40,pady=36,highlightthickness=1,highlightbackground="#d7e2f0")
        card.place(relx=.5,rely=.5,anchor="center",width=420,height=490)
        tk.Label(card,text="🎓",bg=PANEL,fg=BLUE,font=("Segoe UI",34)).pack(pady=(5,5))
        tk.Label(card,text="SIMS SEKOLAH",bg=PANEL,fg=DARK,font=("Segoe UI",22,"bold")).pack()
        tk.Label(card,text="Sistem Manajemen Data Siswa",bg=PANEL,fg=MUTED,font=("Segoe UI",10)).pack(pady=(5,25))
        tk.Label(card,text="USERNAME",bg=PANEL,fg=MUTED,font=("Segoe UI",9,"bold")).pack(anchor="w")
        self.u=self.ent(card);self.u.pack(fill="x",ipady=9,pady=(5,18))
        tk.Label(card,text="PASSWORD",bg=PANEL,fg=MUTED,font=("Segoe UI",9,"bold")).pack(anchor="w")
        self.p=self.ent(card);self.p.configure(show="●");self.p.pack(fill="x",ipady=9,pady=(5,25))
        self.btn(card,"MASUK  →",self.check).pack(fill="x",ipady=3)
        tk.Label(card,text="Akun awal: admin / admin123",bg=PANEL,fg=MUTED,font=("Segoe UI",8)).pack(pady=18)
        self.root.bind("<Return>",lambda e:self.check())
    def check(self):
        if self.db.login(self.u.get().strip(),self.p.get()):
            self.user=self.u.get().strip();self.root.unbind("<Return>");self.home()
        else:messagebox.showerror("Login gagal","Username atau password salah.")
    def home(self):
        self.clear();self.root.configure(bg=BG)
        shell=tk.Frame(self.root,bg=BG);shell.pack(fill="both",expand=True)
        side=tk.Frame(shell,bg="#1e40af",width=220);side.pack(side="left",fill="y");side.pack_propagate(False)
        tk.Label(side,text="◈  SIMS SEKOLAH",bg="#1e40af",fg="white",font=("Segoe UI",16,"bold")).pack(anchor="w",padx=18,pady=(25,5))
        tk.Label(side,text="MANAJEMEN SISWA",bg="#1e40af",fg="#dbeafe",font=("Segoe UI",8,"bold")).pack(anchor="w",padx=20,pady=(0,28))
        self.content=tk.Frame(shell,bg=BG);self.content.pack(side="left",fill="both",expand=True)
        for t,fn in [("▦  Dashboard",self.dashboard),("▤  Data Siswa",self.students),("▧  Ekspor Excel",self.export_xlsx),("▧  Ekspor PDF",self.export_pdf_file)]:
            self.btn(side,t,fn,"#3159ad").pack(fill="x",padx=12,pady=5)
        tk.Frame(side,bg="#1e40af").pack(fill="both",expand=True)
        tk.Label(side,text=f"Login: {self.user}",bg="#1e40af",fg="#dbeafe").pack(anchor="w",padx=18,pady=5)
        self.btn(side,"Keluar",self.logout,RED).pack(fill="x",padx=12,pady=20)
        self.dashboard()
    def logout(self):
        if messagebox.askyesno("Keluar","Keluar dari aplikasi?"):self.login()
    def header(self,title,subtitle):
        tk.Label(self.content,text=title,bg=BG,fg=DARK,font=("Segoe UI",22,"bold")).pack(anchor="w",padx=26,pady=(22,2))
        tk.Label(self.content,text=subtitle,bg=BG,fg=MUTED,font=("Segoe UI",9)).pack(anchor="w",padx=27,pady=(0,18))
    def stat(self,p,title,val,col):
        f=tk.Frame(p,bg="white",padx=18,pady=16,highlightthickness=1,highlightbackground="#d7e2f0")
        tk.Label(f,text=title,bg="white",fg=MUTED,font=("Segoe UI",9,"bold")).pack(anchor="w")
        tk.Label(f,text=str(val),bg="white",fg=col,font=("Segoe UI",25,"bold")).pack(anchor="w",pady=(7,0))
        return f
    def tree(self,p,rows):
        frame=tk.Frame(p,bg=p.cget("bg"));frame.pack(fill="both",expand=True)
        keys=("nis","nama","kelas","jurusan","jk","telepon")
        t=ttk.Treeview(frame,columns=keys,show="headings")
        for k,h in zip(keys,("NIS","Nama Siswa","Kelas","Jurusan","JK","Telepon")):t.heading(k,text=h);t.column(k,width=125)
        sb=ttk.Scrollbar(frame,orient="vertical",command=t.yview);t.configure(yscrollcommand=sb.set)
        t.pack(side="left",fill="both",expand=True);sb.pack(side="right",fill="y")
        for r in rows:t.insert("","end",values=r)
        return t
    def dashboard(self):
        for w in self.content.winfo_children():w.destroy()
        self.header("Dashboard","Ringkasan data siswa tersimpan di MySQL")
        stats=self.db.stats();row=tk.Frame(self.content,bg=BG);row.pack(fill="x",padx=26)
        for title,val,col in [("TOTAL SISWA",stats["total"],BLUE),("KELAS",stats["kelas"],GOLD),("JURUSAN",stats["jurusan"],GREEN)]:
            self.stat(row,title,val,col).pack(side="left",fill="x",expand=True,padx=(0,12))
        panel=tk.Frame(self.content,bg=PANEL,padx=18,pady=16);panel.pack(fill="both",expand=True,padx=26,pady=20)
        tk.Label(panel,text="Data siswa terbaru",bg=PANEL,fg=DARK,font=("Segoe UI",13,"bold")).pack(anchor="w",pady=(0,10))
        self.tree(panel,self.db.get_students()[:10])
    def students(self):
        for w in self.content.winfo_children():w.destroy()
        self.header("Data Siswa","Tambah, edit, hapus, cari, dan filter data siswa")
        top=tk.Frame(self.content,bg=BG);top.pack(fill="x",padx=26,pady=(0,10))
        self.search=self.ent(top);self.search.pack(side="left",fill="x",expand=True,ipady=8,padx=(0,6))
        self.kelas=ttk.Combobox(top,width=12,values=["Semua Kelas"]+self.db.classes());self.kelas.set("Semua Kelas");self.kelas.pack(side="left",padx=5)
        self.jur=ttk.Combobox(top,width=16,values=["Semua Jurusan"]+self.db.majors());self.jur.set("Semua Jurusan");self.jur.pack(side="left",padx=5)
        self.btn(top,"Cari/Filter",self.refresh).pack(side="left",padx=4)
        self.btn(top,"＋ Tambah",lambda:self.form()).pack(side="left",padx=4)
        panel=tk.Frame(self.content,bg=PANEL,padx=10,pady=10);panel.pack(fill="both",expand=True,padx=26)
        self.t=self.tree(panel,[])
        def edit():
            s=self.t.selection()
            if s:self.form(self.t.item(s[0],"values"))
            else:messagebox.showinfo("Info","Pilih siswa terlebih dahulu.")
        def delete():
            s=self.t.selection()
            if not s:return messagebox.showinfo("Info","Pilih siswa terlebih dahulu.")
            r=self.t.item(s[0],"values")
            if messagebox.askyesno("Hapus",f"Hapus data {r[1]}?"):self.db.delete(r[0]);self.refresh()
        self.btn(top,"Edit",edit,"#64748b").pack(side="left",padx=4)
        self.btn(top,"Hapus",delete,RED).pack(side="left",padx=4)
        self.refresh()
    def refresh(self):
        if not hasattr(self,"t"):return
        for i in self.t.get_children():self.t.delete(i)
        k=self.kelas.get();j=self.jur.get()
        for r in self.db.get_students(self.search.get().strip(),None if k=="Semua Kelas" else k,None if j=="Semua Jurusan" else j):self.t.insert("","end",values=r)
    def form(self,data=None):
        w=tk.Toplevel(self.root);w.title("Form Siswa");w.geometry("430x540");w.configure(bg=PANEL);w.transient(self.root);w.grab_set()
        tk.Label(w,text="Form Data Siswa",bg=PANEL,fg=DARK,font=("Segoe UI",16,"bold")).pack(pady=18)
        fields=[("NIS",data[0] if data else ""),("Nama",data[1] if data else ""),("Kelas",data[2] if data else ""),("Jurusan",data[3] if data else ""),("Jenis Kelamin",data[4] if data else "L"),("Telepon",data[5] if data else "")]
        inputs={}
        for name,val in fields:
            tk.Label(w,text=name,bg=PANEL,fg=MUTED,font=("Segoe UI",9)).pack(anchor="w",padx=28,pady=(5,2))
            if name=="Jenis Kelamin":x=ttk.Combobox(w,values=["L","P"],state="readonly");x.set(val or "L")
            else:x=self.ent(w);x.insert(0,str(val))
            x.pack(fill="x",padx=28,ipady=5);inputs[name]=x
        def save():
            v={k:x.get().strip() for k,x in inputs.items()}
            if not v["NIS"] or not v["Nama"] or not v["Kelas"] or not v["Jurusan"]:return messagebox.showerror("Validasi","NIS, nama, kelas, dan jurusan wajib diisi.")
            try:self.db.save(v,data[0] if data else None);w.destroy();self.refresh()
            except Exception as e:messagebox.showerror("Gagal menyimpan",str(e))
        self.btn(w,"Simpan Data",save).pack(fill="x",padx=28,pady=18)
    def export_xlsx(self):
        path=filedialog.asksaveasfilename(defaultextension=".xlsx",filetypes=[("Excel Workbook","*.xlsx")],initialfile="data_siswa.xlsx")
        if path:
            try:export_excel(path,self.db.get_students());messagebox.showinfo("Sukses","Excel berhasil diekspor.")
            except Exception as e:messagebox.showerror("Ekspor gagal",str(e))
    def export_pdf_file(self):
        path=filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF","*.pdf")],initialfile="laporan_siswa.pdf")
        if path:
            try:export_pdf(path,self.db.get_students());messagebox.showinfo("Sukses","PDF berhasil diekspor.")
            except Exception as e:messagebox.showerror("Ekspor gagal",str(e))

if __name__=="__main__":
    root=tk.Tk();App(root);root.mainloop()
