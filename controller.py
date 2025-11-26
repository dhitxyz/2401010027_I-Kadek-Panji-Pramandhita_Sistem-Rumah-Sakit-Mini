from model import RumahSakit, Dokter, Pasien
import view
from rich.console import Console

console = Console()

class Controller:
    def __init__(self, nama_rs="Rumah Sakit Mini"):
        self.rs = RumahSakit(nama_rs)

    def tambah_dokter(self):
        nama = view.input_prompt("Nama Dokter: ").strip()
        umur = view.input_prompt("Umur Dokter: ").strip()
        spesialis = view.input_prompt("Spesialisasi Dokter: ").strip()

        if not umur.isdigit() or int(umur) <= 0:
            view.tampilkan_pesan("[bold red]Umur harus berupa angka positif![/bold red]")
            return

        dokter = Dokter(nama, int(umur), spesialis)
        self.rs.tambah_dokter(dokter)

    def tambah_pasien(self):
        nama = view.input_prompt("Nama Pasien: ").strip()
        umur = view.input_prompt("Umur Pasien: ").strip()
        penyakit = view.input_prompt("Penyakit Pasien: ").strip()

        if not umur.isdigit() or int(umur) <= 0:
            view.tampilkan_pesan("[bold red]Umur harus berupa angka positif![/bold red]")
            return

        pasien = Pasien(nama, int(umur), penyakit)
        self.rs.tambah_pasien(pasien)

    def tampilkan_data(self):
        view.tampilkan_header(self.rs._RumahSakit__nama_rs)
        view.tampilkan_dokter(self.rs._RumahSakit__daftar_dokter)
        view.tampilkan_pasien(self.rs._RumahSakit__daftar_pasien)

    def verifikasi_pasien(self):
        nama_dokter = view.input_prompt("Masukkan nama dokter: ").strip()
        nama_pasien = view.input_prompt("Masukkan nama pasien: ").strip()

        dokter_obj = None
        pasien_obj = None

        for dokter in self.rs._RumahSakit__daftar_dokter:
            if dokter._nama == nama_dokter:
                dokter_obj = dokter
                break

        for pasien in self.rs._RumahSakit__daftar_pasien:
            if pasien._nama == nama_pasien:
                pasien_obj = pasien
                break

        if dokter_obj and pasien_obj:
            view.tampilkan_verifikasi(dokter_obj, pasien_obj)
        else:
            if not dokter_obj:
                view.tampilkan_pesan(f"[bold red]Dokter dengan nama '{nama_dokter}' tidak ditemukan.[/bold red]")
            if not pasien_obj:
                view.tampilkan_pesan(f"[bold red]Pasien dengan nama '{nama_pasien}' tidak ditemukan.[/bold red]")

    def keluar(self):
        self.rs.tutup_database()
        view.tampilkan_pesan("\n[bold green]Terima kasih telah menggunakan Sistem Rumah Sakit Mini![/bold green]")

    def run(self):
        import sys
        while True:
            try:
                console.print("\n[bold cyan]Menu Sistem Rumah Sakit Mini[/bold cyan]", style="bold underline")
                console.print("[1] Tambah Dokter")
                console.print("[2] Tambah Pasien")
                console.print("[3] Tampilkan Data")
                console.print("[4] Verifikasi Pasien oleh Dokter")
                console.print("[5] Keluar")

                pilihan = view.input_prompt("\nMasukkan pilihan Anda (1-5): ").strip()

                if pilihan == '1':
                    self.tambah_dokter()

                elif pilihan == '2':
                    self.tambah_pasien()

                elif pilihan == '3':
                    self.tampilkan_data()

                elif pilihan == '4':
                    self.verifikasi_pasien()

                elif pilihan == '5':
                    self.keluar()
                    break

                else:
                    view.tampilkan_pesan("[bold red]Pilihan tidak valid, silakan pilih antara 1 sampai 5![/bold red]")
            except KeyboardInterrupt:
                view.tampilkan_pesan("\n[bold yellow]Input dibatalkan oleh pengguna, keluar dari program.[/bold yellow]")
                self.keluar()
                sys.exit(0)
