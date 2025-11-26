import sqlite3
from rich.console import Console
from rich.panel import Panel
from rich import box

console = Console()

class DatabaseHelper:
    """
    Class to manage SQLite database connection and operations
    """
    
    def __init__(self, db_name='rumah_sakit.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.buka_koneksi()
        self.buat_tabel()
    
    def buka_koneksi(self):
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            console.print(f"[bold green]✓[/bold green] Koneksi database '[cyan]{self.db_name}[/cyan]' berhasil!", style="bold")
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error koneksi database: {e}", style="bold red")
    
    def buat_tabel(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tabel_dokter (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    umur INTEGER NOT NULL,
                    spesialis TEXT NOT NULL
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tabel_pasien (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    umur INTEGER NOT NULL,
                    penyakit TEXT NOT NULL
                )
            ''')
            
            self.conn.commit()
            console.print("[bold green]✓[/bold green] Tabel database berhasil dibuat/diperiksa!", style="bold")
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error membuat tabel: {e}", style="bold red")
    
    def simpan_dokter(self, nama, umur, spesialis):
        try:
            self.cursor.execute('''
                INSERT INTO tabel_dokter (nama, umur, spesialis) VALUES (?, ?, ?)
            ''', (nama, umur, spesialis))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error menyimpan dokter: {e}", style="bold red")
            return None
    
    def simpan_pasien(self, nama, umur, penyakit):
        try:
            self.cursor.execute('''
                INSERT INTO tabel_pasien (nama, umur, penyakit) VALUES (?, ?, ?)
            ''', (nama, umur, penyakit))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error menyimpan pasien: {e}", style="bold red")
            return None
    
    def ambil_semua_dokter(self):
        try:
            self.cursor.execute('SELECT id, nama, umur, spesialis FROM tabel_dokter')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error mengambil data dokter: {e}", style="bold red")
            return []
    
    def cek_dokter_ada(self, nama):
        try:
            self.cursor.execute('SELECT id FROM tabel_dokter WHERE nama = ?', (nama,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error mengecek dokter: {e}", style="bold red")
            return False
    
    def cek_pasien_ada(self, nama):
        try:
            self.cursor.execute('SELECT id FROM tabel_pasien WHERE nama = ?', (nama,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error mengecek pasien: {e}", style="bold red")
            return False
    
    def ambil_semua_pasien(self):
        try:
            self.cursor.execute('SELECT id, nama, umur, penyakit FROM tabel_pasien')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error mengambil data pasien: {e}", style="bold red")
            return []
    
    def tutup_koneksi(self):
        if self.conn:
            self.conn.close()
            console.print("[bold green]✓[/bold green] Koneksi database ditutup!", style="bold")

class Orang:
    def __init__(self, nama, umur):
        self._nama = nama
        self._umur = umur
    
    def get_nama(self):
        return self._nama
    
    def get_umur(self):
        return self._umur

class Pasien(Orang):
    def __init__(self, nama, umur, penyakit):
        super().__init__(nama, umur)
        self.__penyakit = penyakit
    
    def get_penyakit(self):
        return self.__penyakit

class Dokter(Orang):
    def __init__(self, nama, umur, spesialis):
        super().__init__(nama, umur)
        self.__spesialis = spesialis
    
    def get_spesialis(self):
        return self.__spesialis

class RumahSakit:
    def __init__(self, nama_rs):
        self.__nama_rs = nama_rs
        self.__daftar_pasien = []
        self.__daftar_dokter = []
        self.db = DatabaseHelper()
        self.muat_data_dari_database()
    
    def tambah_pasien(self, pasien):
        for p in self.__daftar_pasien:
            if p.get_nama() == pasien.get_nama():
                return
        if self.db.cek_pasien_ada(pasien.get_nama()):
            return
        pasien_id = self.db.simpan_pasien(pasien.get_nama(), pasien.get_umur(), pasien.get_penyakit())
        if pasien_id:
            self.__daftar_pasien.append(pasien)
    
    def tambah_dokter(self, dokter):
        for d in self.__daftar_dokter:
            if d.get_nama() == dokter.get_nama():
                return
        if self.db.cek_dokter_ada(dokter.get_nama()):
            return
        dokter_id = self.db.simpan_dokter(dokter.get_nama(), dokter.get_umur(), dokter.get_spesialis())
        if dokter_id:
            self.__daftar_dokter.append(dokter)
    
    def muat_data_dari_database(self):
        data_dokter = self.db.ambil_semua_dokter()
        for _id, nama, umur, spesialis in data_dokter:
            sudah_ada = any(d.get_nama() == nama for d in self.__daftar_dokter)
            if not sudah_ada:
                self.__daftar_dokter.append(Dokter(nama, umur, spesialis))
        data_pasien = self.db.ambil_semua_pasien()
        for _id, nama, umur, penyakit in data_pasien:
            sudah_ada = any(p.get_nama() == nama for p in self.__daftar_pasien)
            if not sudah_ada:
                self.__daftar_pasien.append(Pasien(nama, umur, penyakit))
    
    def tampilkan_data(self):
        view.tampilkan_header(self.__nama_rs)
        view.tampilkan_dokter(self.__daftar_dokter)
        view.tampilkan_pasien(self.__daftar_pasien)
    
    def tutup_database(self):
        self.db.tutup_koneksi()
