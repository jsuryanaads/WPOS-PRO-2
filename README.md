# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.0.0**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Teknologi
- Python 3.11+
- PySide6
- SQLite
- SQLAlchemy
- PyInstaller
- Inno Setup

## Alur kasir
Barcode → Keranjang → Diskon → Pembayaran → Kembalian → Stok berkurang → Transaksi tersimpan → Cetak struk.

## Modul
- Login
- Dashboard
- Kasir
- Produk
- Kategori dan Satuan
- Stok & Mutasi
- Pembelian
- Supplier
- Kas
- Pelanggan
- Laporan
- Pengaturan Toko
- Printer
- Backup / Restore
- User & Role Access

## Integritas transaksi
- Invoice unik.
- Barcode unik.
- Stok tidak boleh negatif.
- Penjualan diproses atomically.
- Penjualan CASH menambah kas.
- QRIS/TRANSFER/DEBIT tidak menambah kas.
- Pembayaran non-tunai harus sama persis dengan total.
- Kembalian hanya untuk CASH.
- Mutasi stok dicatat untuk penjualan, pembelian dan penyesuaian stok.

## Keamanan
- Password menggunakan PBKDF2-SHA256 dengan salt acak.
- User inactive tidak dapat login.
- Minimal satu Administrator aktif dipertahankan.
- Ganti password default sebelum produksi.

## Default login
- Username: `admin`
- Password: `admin123`

## Data Windows
Saat dijalankan sebagai EXE, database dan backup disimpan di:
`%LOCALAPPDATA%\\WPOS PRO 2`

## Menjalankan dari source
```bat
python -m app.main
```

## Testing
```bat
pytest -q
```

## Build EXE
Gunakan:
```bat
build.bat
```

Asset branding yang digunakan:
- `assets\\branding\\wpos_logo.png`
- `assets\\branding\\wpos_icon.ico`

Hasil build:
`dist\\WPOS PRO 2\\WPOS PRO 2.exe`

## Installer
Setelah EXE berhasil dibuat, compile `installer.iss` menggunakan Inno Setup.

Hasil installer:
`installer\\WPOS_PRO_2_Setup.exe`

## CI
GitHub Actions menjalankan compile check dan test suite pada push/PR. Windows build memverifikasi source, test, EXE, associated icon, serta asset branding.

## Status
**WPOS PRO 2 — kandidat release setelah CI PASS dan verifikasi Windows/thermal printer/installer.**
