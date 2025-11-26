from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def tampilkan_header(nama_rs):
    header = Panel(
        f"[bold white]{nama_rs}[/bold white]",
        title="[bold cyan]Data Rumah Sakit[/bold cyan]",
        border_style="cyan",
        box=box.DOUBLE,
        width=78
    )
    console.print("\n")
    console.print(header)

def tampilkan_dokter(daftar_dokter):
    table_dokter = Table(
        title="[bold green]Daftar Dokter[/bold green]",
        box=box.ROUNDED, 
        border_style="green",
        show_header=True,
        header_style="bold green"
    )
    table_dokter.add_column("No", style="cyan", width=5, justify="center")
    table_dokter.add_column("Nama", style="bold cyan", width=25)
    table_dokter.add_column("Umur", style="yellow", width=10, justify="center")
    table_dokter.add_column("Spesialis", style="green", width=25)

    if daftar_dokter:
        for idx, d in enumerate(daftar_dokter, 1):
            table_dokter.add_row(
                str(idx),
                d.get_nama(),
                str(d.get_umur()),
                d.get_spesialis()
            )
    else:
        table_dokter.add_row("", "[dim](Belum ada data dokter)[/dim]", "", "", style="dim")

    console.print(table_dokter)

def tampilkan_pasien(daftar_pasien):
    table_pasien = Table(
        title="[bold blue]Daftar Pasien[/bold blue]", 
        box=box.ROUNDED, 
        border_style="blue",
        show_header=True,
        header_style="bold blue"
    )
    table_pasien.add_column("No", style="cyan", width=5, justify="center")
    table_pasien.add_column("Nama", style="bold cyan", width=25)
    table_pasien.add_column("Umur", style="yellow", width=10, justify="center")
    table_pasien.add_column("Penyakit", style="red", width=25)

    if daftar_pasien:
        for idx, p in enumerate(daftar_pasien, 1):
            table_pasien.add_row(
                str(idx),
                p.get_nama(),
                str(p.get_umur()),
                p.get_penyakit()
            )
    else:
        table_pasien.add_row("", "[dim](Belum ada data pasien)[/dim]", "", "", style="dim")

    console.print(table_pasien)

def tampilkan_info_orang(orang_obj, tipe="Orang"):
    from rich.text import Text

    if tipe == "Dokter":
        from rich.panel import Panel
        panel = Panel(
            f"[bold cyan]Nama:[/bold cyan] {orang_obj.get_nama()}\n"
            f"[bold yellow]Umur:[/bold yellow] {orang_obj.get_umur()}\n"
            f"[bold green]Spesialis:[/bold green] {orang_obj.get_spesialis()}",
            title="[bold green]Dokter[/bold green]",
            border_style="green",
            box=box.ROUNDED
        )
        console.print(panel)
    elif tipe == "Pasien":
        from rich.panel import Panel
        panel = Panel(
            f"[bold cyan]Nama:[/bold cyan] {orang_obj.get_nama()}\n"
            f"[bold yellow]Umur:[/bold yellow] {orang_obj.get_umur()}\n"
            f"[bold red]Penyakit:[/bold red] {orang_obj.get_penyakit()}",
            title="[bold blue]Pasien[/bold blue]",
            border_style="blue",
            box=box.ROUNDED
        )
        console.print(panel)
    else:
        console.print(f"Nama: {orang_obj.get_nama()}, Umur: {orang_obj.get_umur()}")

def tampilkan_verifikasi(dokter, pasien):
    from rich.panel import Panel
    panel = Panel(
        f"[bold green]Dokter {dokter.get_nama()}[/bold green] memverifikasi pasien [bold cyan]{pasien.get_nama()}[/bold cyan] "
        f"dengan penyakit [bold red]{pasien.get_penyakit()}[/bold red]",
        title="[bold yellow]Verifikasi Pasien[/bold yellow]",
        border_style="yellow",
        box=box.ROUNDED,
        width=78
    )
    console.print(panel)

def tampilkan_pesan(pesan, style="bold"):
    console.print(pesan, style=style)

def input_prompt(prompt):
    return console.input(prompt)
