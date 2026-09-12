# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.7.15**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Perubahan terbaru 2.7.15
- Menstabilkan CI dengan menjadikan workflow Windows Build dan Windows Installer sebagai **manual dispatch** sementara runner Windows GitHub mengalami kegagalan sebelum step pertama.
- Menambahkan workflow independen `ci-health.yml` pada Ubuntu untuk memvalidasi checkout, Python, dependency, compile dan pytest tanpa bergantung pada Windows runner.
- Menyinkronkan config, installer dan regression test ke versi **2.7.15**.
- Tidak mengubah UI, authentication flow, database, schema, atau business logic.

## Build Windows aktif
- `windows-build.yml`: build EXE Windows otomatis pada push ke `main` dan tetap tersedia melalui `workflow_dispatch`.
- `windows-installer.yml`: build installer Windows otomatis pada push ke `main` dan tetap tersedia melalui `workflow_dispatch`.
- Kedua workflow menggunakan `windows-2022`, Python 3.12, compileall, pytest, PyInstaller, pemeriksaan branding, dan validasi output.
- Artifact build: `WPOS-PRO-2-Windows`.
- Artifact installer: `WPOS-PRO-2-Installer`.

## Perubahan 2.7.14
- Memperbaiki jalur CI Windows dengan mengganti runner `windows-latest` menjadi `windows-2022` pada workflow Build dan Installer.
- Menambahkan diagnostic runner pada workflow Windows agar identitas runner/image dapat terlihat jika terjadi kegagalan sebelum proses build.
- Tidak mengubah UI, authentication flow, database, schema, atau business logic.

## 14 halaman
1. Dashboard
2. Kasir
3. Produk
4. Stok & Mutasi
5. Pembelian
6. Kas
7. Laporan
8. Pengaturan Toko
9. Printer
10. Backup / Restore
11. Kategori
12. Satuan
13. Supplier
14. Pelanggan

## Struktur sidebar
- **OPERASIONAL:** Dashboard, Kasir, Produk, Stok & Mutasi, Pembelian.
- **KEUANGAN:** Kas, Laporan.
- **DATA MASTER:** Pelanggan, Supplier, Kategori, Satuan.
- **SYSTEM:** Pengaturan Toko, Printer, Backup / Restore.
- Text-only tanpa ikon dekoratif.
- Lebar sidebar 230 px.
- Active menu dan hover mengikuti tema.

## Struktur Headerbar FINAL
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ KASIR                    TOKO SEMBAKO SAPNI        Selamat datang, Admin    │
│ Transaksi cepat · barcode first                    12 September 2026        │
│                                                     Sabtu                    │
└─────────────────────────────────────────────────────────────────────────────┘
```
- **Kiri:** halaman aktif + subtitle/hint.
- **Tengah:** nama toko dari `store_name`.
- **Kanan:** pengguna + tanggal + hari otomatis.
- Status OFFLINE/DATABASE LOKAL tidak ditampilkan di Headerbar.

## Struktur Kasir PRO
- **Input Produk:** Barcode / Cari Produk, Qty, Tambah dan Cari Produk.
- **Keranjang Transaksi:** Barcode, Produk, Qty, Harga, Subtotal.
- **Kontrol Keranjang:** `− QTY`, `+ QTY`, `HAPUS ITEM`.
- **Pembayaran:** Total, Diskon, Metode, Bayar, Kembalian.
- **Kontrol Transaksi:** Parkir, Transaksi Parkir, Batal Transaksi, Riwayat dan Bayar & Cetak.
- Nilai transaksi/database tetap Decimal.
- Qty bulat pada struk ditampilkan tanpa `.0`.

## Produk
- Tambah, Edit, Nonaktifkan, Hapus aman.
- Produk dengan histori transaksi/mutasi tidak dapat dihapus permanen.
- Tabel Produk menampilkan: ID, Barcode, Nama, Kategori, Satuan, Beli, Jual, Stok, Status.
- Stok bulat ditampilkan tanpa pemisah desimal palsu, misalnya `20` bukan `20.000`.
- Status menunjukkan `AKTIF` atau `NONAKTIF`.

## CRUD Master
- Kategori: Tambah, Edit, Simpan, Hapus.
- Satuan: Tambah, Edit, Simpan, Hapus.
- Supplier: Tambah, Edit, Simpan, Hapus.
- Pelanggan: Tambah, Edit, Simpan, Hapus.

## Kasir
- Cari Produk berdasarkan nama/barcode.
- Scanner barcode + Enter.
- Qty − / +.
- Hapus item dan batal transaksi dengan konfirmasi.
- Diskon transaksi.
- Bayar dan Kembalian live.
- Pembayaran non-CASH mengikuti total.
- Riwayat dan cetak ulang struk.
- Parkir transaksi selama sesi aplikasi.
- Shortcut F4, F8, F9, F10 dan Escape.

## Reset Data
- **RESET TRANSAKSI & STOK** mempertahankan master bisnis.
- **RESET SEMUA DATA BISNIS** membersihkan master bisnis dan transaksi.
- User dan pengaturan toko dipertahankan.
- Konfirmasi wajib mengetik `RESET`.

## Integritas transaksi
- Invoice unik.
- Barcode unik.
- Stok tidak boleh negatif.
- Penjualan atomic.
- CASH menambah kas; QRIS/TRANSFER/DEBIT tidak menambah kas.
- Pembayaran non-tunai harus sama dengan total.
- Kembalian hanya CASH.
- Mutasi stok dicatat.

## Keamanan
- Password PBKDF2-SHA256 dengan salt acak.
- User inactive tidak dapat login.
- Minimal satu Administrator aktif.

## Default login
- Username: `admin`
- Password: `admin123`

## Data Windows
Saat EXE dijalankan, database dan backup berada di `%LOCALAPPDATA%\\WPOS PRO 2`.

## Menjalankan source
```bat
python -m app.main
```

## Testing
```bat
pytest -q
```

## Build EXE
```bat
build.bat
```
Hasil: `dist\\WPOS PRO 2\\WPOS PRO 2.exe`

## Installer
Compile `installer.iss` menggunakan Inno Setup.
Hasil: `installer\\WPOS_PRO_2_Setup.exe`

## CI
- `ci-health.yml`: health check otomatis di Ubuntu untuk compile dan pytest.
- `windows-build.yml`: build EXE Windows otomatis pada push ke `main` atau melalui **workflow_dispatch**.
- `windows-installer.yml`: build installer Windows otomatis pada push ke `main` atau melalui **workflow_dispatch**.
- Workflow Windows menggunakan `windows-2022` dan diagnostic runner.
- Artifact hasil build tersedia pada masing-masing workflow jika seluruh validasi berhasil.

## Tema
- **Dark Mode** — default.
- **Light Mode**.
- Tema lama dihapus dan key invalid fallback ke DARK.

## Numeric Input
- Input desktop angka bulat menggunakan langkah 1.
- `1` tetap `1`, `2` tetap `2`, `10` tetap `10`.
- Tampilan stok bulat dinormalisasi tanpa mengubah database.
- Nilai pecahan yang benar tetap dipertahankan.
- Tidak ada faktor ×1.000.

## UI
- Sidebar text-only 230 px.
- Headerbar tiga zona: Context kiri, Nama Toko tengah, Pengguna + Tanggal kanan.
- Kasir menggunakan struktur Input Produk → Keranjang + Pembayaran → Kontrol Transaksi.
- Form Produk, Pembelian, Supplier dan Pelanggan menggunakan popup hybrid.
- Kategori dan Satuan menggunakan form inline/horizontal.
- Footer: **Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana**.
- Login tidak mengulang versi aplikasi karena versi sudah tersedia di Footer.

## Excel Produk
- Export `.xlsx`.
- Template `.xlsx`.
- Import Tambah atau Update berdasarkan Barcode.
- Update tidak mengubah stok berjalan.

## Versioning
- Fitur/perubahan besar: naik MINOR.
- Perbaikan/perubahan kecil: naik PATCH.
- Setiap perubahan source, config, installer, test atau dokumentasi dicatat di README.

## Changelog
### 2.7.15
- Menjadikan Windows Build dan Windows Installer sebagai manual dispatch sementara.
- Menambahkan `ci-health.yml` untuk health check otomatis di Ubuntu.
- Menyinkronkan config, installer dan regression test ke **2.7.15**.
- Tidak mengubah schema/database/business logic.

### 2.7.14
- Mengubah runner Windows dari `windows-latest` menjadi `windows-2022` pada Build dan Installer.
- Menambahkan diagnostic runner untuk memperjelas image/runner bila job gagal sebelum build.
- Menyinkronkan `app/config.py`, `installer.iss`, dan regression test ke **2.7.14**.
- Tidak mengubah schema/database/business logic.

### 2.7.13
- Memperbaiki test `test_version_and_docs_are_synchronized` yang masih mengharapkan versi **2.7.10**.
- Menyinkronkan test dengan versi aplikasi baru.
- Menyinkronkan `app/config.py` dan `installer.iss` ke **2.7.13**.
- Perubahan ini dibuat untuk memperbaiki kegagalan CI run #294.
- Tidak mengubah schema/database/business logic.

### 2.7.12
- Menghapus versi dari kartu Login agar tidak duplikat dengan Footer.
- Mempertahankan **WPOS PRO 2** dan **Point of Sale** pada Login.
- Menyinkronkan config dan installer ke **2.7.12**.
- Memperbarui regression test Login.
- Tidak mengubah authentication flow, database, schema, atau business logic.

### 2.7.11
- Mendesain ulang struktur Login.
- Menambahkan mode Offline / Database Lokal, placeholder input, tombol password dan default action MASUK.

### 2.7.10
- Memperbaiki refresh tampilan Stok Produk agar normalisasi `20.000 → 20` dilakukan setelah reload tabel.
- Menambahkan deferred refresh saat menu Produk dibuka kembali.
- Menyinkronkan version config dan installer ke **2.7.10**.
- Tidak mengubah schema/database/business logic.

### 2.7.9
- Memperbaiki presentasi Stok tabel Produk agar angka bulat tidak tampil sebagai `20.000`.
- Menambahkan kolom Status `AKTIF` / `NONAKTIF`.
- Menambahkan `app/ui/product_display.py`.
- Memanggil normalisasi tabel Produk dari UI refresh.
- Tidak mengubah schema/database/business logic.

### 2.7.8
- Menambahkan struktur Headerbar final dan sumber nama toko dari pengaturan.

### 2.7.7
- Menata struktur Kasir PRO dan kontrol transaksi.

### 2.7.6
- Menata Headerbar tiga zona.

### 2.7.5
- Memperbaiki sidebar text-only dan area Keranjang Kasir.
- Menghilangkan `.0` pada Qty struk.

### 2.7.4
- Penyempurnaan visual sidebar.

### 2.7.3
- Kembalian Kasir live saat nominal Bayar berubah.

### 2.7.2
- Memperbaiki crash `form_layouts.py` saat mengakses `load_products` pada widget halaman.

### 2.7.1
- Hapus Produk aman dengan perlindungan histori.

### 2.7.0
- Pengembangan workflow Kasir PRO dan Parkir Transaksi.

### 2.6.0
- Pencarian produk, Qty, hapus item, batal transaksi, riwayat, cetak ulang dan shortcut.

### 2.5.1
- Penyempurnaan section sidebar dan styling Dark/Light Mode.

### 2.5.0
- Reset Data dengan konfirmasi dua tahap.

## Arsitektur
- `app/ui/modern_main_window.py` — shell/sidebar/topbar/stack.
- `app/ui/main_window.py` — halaman dan workflow bisnis.
- `app/ui/premium_cashier.py` — UI Kasir.
- `app/ui/cashier_structure.py` — struktur presentasi Kasir.
- `app/ui/headerbar.py` — struktur Headerbar.
- `app/ui/product_display.py` — presentasi Stok dan Status tabel Produk.
- `app/ui/master_data.py` — CRUD master data.
- `app/ui/form_layouts.py` — hybrid form, Excel, reset dan kontrol Produk.
- `app/ui/global_ui.py` — aturan global UI.
- `app/ui/theme_shell.py` — palette dan styling.
- `app/services/product_delete.py` — penghapusan Produk aman.
- `app/services/receipt_display.py` — presentasi Qty struk.
