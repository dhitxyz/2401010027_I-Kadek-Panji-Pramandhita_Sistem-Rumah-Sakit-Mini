import sqlite3
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.text import Text

# Inisialisasi console untuk rich
console = Console()

# ============================================
# KELAS DATABASE HELPER - Mengelola SQLite
# ============================================
class DatabaseHelper:
    """
    Kelas untuk mengelola koneksi dan operasi database SQLite
    Database akan disimpan dalam file 'rumah_sakit.db'
    """
    
    def __init__(self, db_name='rumah_sakit.db'):
        """
        Inisialisasi koneksi database
        db_name: nama file database (default: rumah_sakit.db)
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.buka_koneksi()
        self.buat_tabel()
    
    def buka_koneksi(self):
        """Membuka koneksi ke database SQLite"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            console.print(f"[bold green]✓[/bold green] Koneksi database '[cyan]{self.db_name}[/cyan]' berhasil!", style="bold")
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error koneksi database: {e}", style="bold red")
    
    def buat_tabel(self):
        """
        Membuat tabel-tabel yang diperlukan jika belum ada:
        - tabel_dokter: menyimpan data dokter
        - tabel_pasien: menyimpan data pasien
        """
        try:
            # Tabel untuk menyimpan data dokter
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tabel_dokter (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    umur INTEGER NOT NULL,
                    spesialis TEXT NOT NULL
                )
            ''')
            
            # Tabel untuk menyimpan data pasien
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tabel_pasien (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT NOT NULL,
                    umur INTEGER NOT NULL,
                    penyakit TEXT NOT NULL
                )
            ''')
            
            # Simpan perubahan ke database
            self.conn.commit()
            console.print("[bold green]✓[/bold green] Tabel database berhasil dibuat/diperiksa!", style="bold")
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error membuat tabel: {e}", style="bold red")
    
    def simpan_dokter(self, nama, umur, spesialis):
        """
        Menyimpan data dokter ke database
        Returns: ID dari dokter yang baru disimpan
        """
        try:
            self.cursor.execute('''
                INSERT INTO tabel_dokter (nama, umur, spesialis)
                VALUES (?, ?, ?)
            ''', (nama, umur, spesialis))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error menyimpan dokter: {e}", style="bold red")
            return None
    
    def simpan_pasien(self, nama, umur, penyakit):
        """
        Menyimpan data pasien ke database
        Returns: ID dari pasien yang baru disimpan
        """
        try:
            self.cursor.execute('''
                INSERT INTO tabel_pasien (nama, umur, penyakit)
                VALUES (?, ?, ?)
            ''', (nama, umur, penyakit))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error menyimpan pasien: {e}", style="bold red")
            return None
    
    def ambil_semua_dokter(self):
        """
        Mengambil semua data dokter dari database
        Returns: List of tuples (id, nama, umur, spesialis)
        """
        try:
            self.cursor.execute('SELECT id, nama, umur, spesialis FROM tabel_dokter')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error mengambil data dokter: {e}", style="bold red")
            return []

    def cek_dokter_ada(self, nama):
        """
        Mengecek apakah dokter dengan nama tertentu sudah ada di database
        Returns: True jika ada, False jika tidak
        """
        try:
            self.cursor.execute('SELECT id FROM tabel_dokter WHERE nama = ?', (nama,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error mengecek dokter: {e}", style="bold red")
            return False

    def cek_pasien_ada(self, nama):
        """
        Mengecek apakah pasien dengan nama tertentu sudah ada di database
        Returns: True jika ada, False jika tidak
        """
        try:
            self.cursor.execute('SELECT id FROM tabel_pasien WHERE nama = ?', (nama,))
            return self.cursor.fetchone() is not None
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error mengecek pasien: {e}", style="bold red")
            return False
    
    def ambil_semua_pasien(self):
        """
        Mengambil semua data pasien dari database
        Returns: List of tuples (id, nama, umur, penyakit)
        """
        try:
            self.cursor.execute('SELECT id, nama, umur, penyakit FROM tabel_pasien')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            console.print(f"[bold red]✗[/bold red] Error mengambil data pasien: {e}", style="bold red")
            return []
    
    def tutup_koneksi(self):
        """Menutup koneksi database"""
        if self.conn:
            self.conn.close()
            console.print("[bold green]✓[/bold green] Koneksi database ditutup!", style="bold")


# ============================================
# KELAS ORANG (Base Class)
# ============================================
class Orang:
    def __init__(self, nama, umur):
        self._nama = nama       # encapsulation (atribut dibuat private)
        self._umur = umur

    def show_info(self):
        console.print(f"[bold cyan]Nama:[/bold cyan] {self._nama}, [bold yellow]Umur:[/bold yellow] {self._umur}")


# Kelas Pasien (turunan dari Class Orang)
class Pasien(Orang):
    def __init__(self, nama, umur, penyakit):
        super().__init__(nama, umur)
        self.__penyakit = penyakit  

    # polymorphism override method show_info
    def show_info(self):
        panel = Panel(
            f"[bold cyan]Nama:[/bold cyan] {self._nama}\n"
            f"[bold yellow]Umur:[/bold yellow] {self._umur}\n"
            f"[bold red]Penyakit:[/bold red] {self.__penyakit}",
            title="[bold blue]Pasien[/bold blue]",
            border_style="blue",
            box=box.ROUNDED
        )
        console.print(panel)


# Kelas Dokter (turunan dari Class Orang) 
class Dokter(Orang):
    def __init__(self, nama, umur, spesialis):
        super().__init__(nama, umur)
        self.__spesialis = spesialis

    def show_info(self):   
        panel = Panel(
            f"[bold cyan]Nama:[/bold cyan] {self._nama}\n"
            f"[bold yellow]Umur:[/bold yellow] {self._umur}\n"
            f"[bold green]Spesialis:[/bold green] {self.__spesialis}",
            title="[bold green]Dokter[/bold green]",
            border_style="green",
            box=box.ROUNDED
        )
        console.print(panel)

    def verifikasi_pasien(self, pasien):
        panel = Panel(
            f"[bold green]Dokter {self._nama}[/bold green] memverifikasi pasien [bold cyan]{pasien._nama}[/bold cyan] "
            f"dengan penyakit [bold red]{pasien._Pasien__penyakit}[/bold red]",
            title="[bold yellow]Verifikasi Pasien[/bold yellow]",
            border_style="yellow",
            box=box.ROUNDED,
            width=78
        )
        console.print(panel)

class RumahSakit:
    """
    Kelas Rumah Sakit dengan integrasi SQLite Database
    Data akan otomatis disimpan dan dimuat dari database
    """
    def __init__(self, nama_rs):
        self.__nama_rs = nama_rs
        self.__daftar_pasien = []
        self.__daftar_dokter = []
        
        # Inisialisasi database helper
        self.db = DatabaseHelper()
        
        # Muat data yang sudah ada dari database
        self.muat_data_dari_database()
    
    def tambah_pasien(self, pasien):
        """
        Menambahkan pasien ke daftar dan menyimpan ke database
        """
        # Cek apakah pasien sudah ada di memory (berdasarkan nama)
        for p in self.__daftar_pasien:
            if p._nama == pasien._nama:
                console.print(f"[bold yellow]⚠[/bold yellow] Pasien [cyan]{pasien._nama}[/cyan] sudah ada di daftar, tidak ditambahkan lagi.", style="bold")
                return
        
        # Cek apakah pasien sudah ada di database
        if self.db.cek_pasien_ada(pasien._nama):
            console.print(f"[bold yellow]⚠[/bold yellow] Pasien [cyan]{pasien._nama}[/cyan] sudah ada di database, tidak ditambahkan lagi.", style="bold")
            return

        # Simpan ke database SQLite
        pasien_id = self.db.simpan_pasien(
            pasien._nama,
            pasien._umur,
            pasien._Pasien__penyakit
        )

        # Tambahkan ke daftar di memory
        if pasien_id:
            self.__daftar_pasien.append(pasien)
            console.print(f"[bold green]✓[/bold green] Pasien [cyan]{pasien._nama}[/cyan] berhasil disimpan ke database (ID: [yellow]{pasien_id}[/yellow])", style="bold")
    
    def tambah_dokter(self, dokter):
        """
        Menambahkan dokter ke daftar dan menyimpan ke database
        """
        # Cek apakah dokter sudah ada di memory (berdasarkan nama)
        for d in self.__daftar_dokter:
            if d._nama == dokter._nama:
                console.print(f"[bold yellow]⚠[/bold yellow] Dokter [cyan]{dokter._nama}[/cyan] sudah ada di daftar, tidak ditambahkan lagi.", style="bold")
                return
        
        # Cek apakah dokter sudah ada di database
        if self.db.cek_dokter_ada(dokter._nama):
            console.print(f"[bold yellow]⚠[/bold yellow] Dokter [cyan]{dokter._nama}[/cyan] sudah ada di database, tidak ditambahkan lagi.", style="bold")
            return

        # Simpan ke database SQLite
        dokter_id = self.db.simpan_dokter(
            dokter._nama,
            dokter._umur,
            dokter._Dokter__spesialis
        )

        # Tambahkan ke daftar di memory
        if dokter_id:
            self.__daftar_dokter.append(dokter)
            console.print(f"[bold green]✓[/bold green] Dokter [cyan]{dokter._nama}[/cyan] berhasil disimpan ke database (ID: [yellow]{dokter_id}[/yellow])", style="bold")
    
    def muat_data_dari_database(self):
        """
        Memuat semua data dari database SQLite ke memory
        Method ini dipanggil saat inisialisasi RumahSakit
        Pastikan tidak ada duplikasi dengan mengecek nama sebelum menambahkan
        """
        # Muat data dokter dari database
        data_dokter = self.db.ambil_semua_dokter()
        for (id_dokter, nama, umur, spesialis) in data_dokter:
            # Cek apakah dokter dengan nama yang sama sudah ada di memory
            sudah_ada = False
            for d in self.__daftar_dokter:
                if d._nama == nama:
                    sudah_ada = True
                    break
            if not sudah_ada:
                dokter = Dokter(nama, umur, spesialis)
                self.__daftar_dokter.append(dokter)
        
        # Muat data pasien dari database
        data_pasien = self.db.ambil_semua_pasien()
        for (id_pasien, nama, umur, penyakit) in data_pasien:
            # Cek apakah pasien dengan nama yang sama sudah ada di memory
            sudah_ada = False
            for p in self.__daftar_pasien:
                if p._nama == nama:
                    sudah_ada = True
                    break
            if not sudah_ada:
                pasien = Pasien(nama, umur, penyakit)
                self.__daftar_pasien.append(pasien)
        
        if data_dokter or data_pasien:
            console.print(
                f"[bold green]✓[/bold green] Data berhasil dimuat dari database: "
                f"[green]{len(self.__daftar_dokter)}[/green] dokter, [blue]{len(self.__daftar_pasien)}[/blue] pasien",
                style="bold"
            )
    
    def tampilkan_data(self):
        """
        Menampilkan semua data dari memory
        (Data sudah dimuat dari database saat inisialisasi)
        """
        # Header utama
        header = Panel(
            f"[bold white]{self.__nama_rs}[/bold white]",
            title="[bold cyan]Data Rumah Sakit[/bold cyan]",
            border_style="cyan",
            box=box.DOUBLE,
            width=78
        )
        console.print("\n")
        console.print(header)
        
        # Tabel Dokter
        table_dokter = Table(title="[bold green]Daftar Dokter[/bold green]", 
                            box=box.ROUNDED, 
                            border_style="green",
                            show_header=True,
                            header_style="bold green")
        table_dokter.add_column("No", style="cyan", width=5, justify="center")
        table_dokter.add_column("Nama", style="bold cyan", width=25)
        table_dokter.add_column("Umur", style="yellow", width=10, justify="center")
        table_dokter.add_column("Spesialis", style="green", width=25)
        
        if self.__daftar_dokter:
            for idx, d in enumerate(self.__daftar_dokter, 1):
                table_dokter.add_row(
                    str(idx),
                    d._nama,
                    str(d._umur),
                    d._Dokter__spesialis
                )
        else:
            table_dokter.add_row("", "[dim](Belum ada data dokter)[/dim]", "", "", style="dim")
        
        console.print(table_dokter)
        
        # Tabel Pasien
        table_pasien = Table(title="[bold blue]Daftar Pasien[/bold blue]", 
                            box=box.ROUNDED, 
                            border_style="blue",
                            show_header=True,
                            header_style="bold blue")
        table_pasien.add_column("No", style="cyan", width=5, justify="center")
        table_pasien.add_column("Nama", style="bold cyan", width=25)
        table_pasien.add_column("Umur", style="yellow", width=10, justify="center")
        table_pasien.add_column("Penyakit", style="red", width=25)
        
        if self.__daftar_pasien:
            for idx, p in enumerate(self.__daftar_pasien, 1):
                table_pasien.add_row(
                    str(idx),
                    p._nama,
                    str(p._umur),
                    p._Pasien__penyakit
                )
        else:
            table_pasien.add_row("", "[dim](Belum ada data pasien)[/dim]", "", "", style="dim")
        
        console.print(table_pasien)
    
    def tutup_database(self):
        """Menutup koneksi database (dipanggil saat selesai)"""
        self.db.tutup_koneksi()


rs = RumahSakit("Panji Sejahtera")


dokter1 = Dokter("dr. Panji", 45, "Penyakit Dalam")
dokter2 = Dokter("dr. Rifqi", 45, "Penyakit Hati")

pasien1 = Pasien("Andi", 25, "Demam")
pasien2 = Pasien("Jaka", 25, "Stroke")

rs.tambah_dokter(dokter1)
rs.tambah_dokter(dokter2)
rs.tambah_pasien(pasien1)
rs.tambah_pasien(pasien2)

rs.tampilkan_data()

console.print("\n")
dokter2.verifikasi_pasien(pasien2)

# Tutup koneksi database saat selesai
footer = Panel(
    "[bold green]Sistem Rumah Sakit Mini - Selesai[/bold green]",
    border_style="green",
    box=box.DOUBLE,
    width=78
)
console.print(footer)
rs.tutup_database()