# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.7.1**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Role
- **ADMIN** — akses penuh dan fungsi administrasi.
- **KASIR** — akses operasional kasir terbatas.

Role PENGELOLA dan TEKNISI telah dihapus dari permission policy. Schema users tetap dipertahankan untuk kompatibilitas data.

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

## Struktur Sidebar
- **OPERASIONAL** — Dashboard, Kasir, Produk, Stok & Mutasi, Pembelian.
- **KEUANGAN** — Kas, Laporan.
- **DATA MASTER** — Pelanggan, Supplier, Kategori, Satuan.
- **SYSTEM** — Pengaturan Toko, Printer, Backup / Restore.

Sidebar tetap text-only. Section memakai background theme-aware yang halus dan SYSTEM memiliki jarak visual lebih besar.

## Produk
Fitur Produk saat ini:
- Tambah produk.
- Edit produk.
- Nonaktifkan produk.
- **Hapus Produk permanen** untuk produk yang belum memiliki histori.
- Export, Import dan Template Excel.
- Form Produk menggunakan popup hybrid.

### Aturan Hapus Produk
Penghapusan permanen hanya diperbolehkan jika produk **belum mempunyai histori penjualan, pembelian, atau mutasi stok**. Jika sudah mempunyai histori, aplikasi menolak penghapusan dan mengarahkan penggunaan **Nonaktifkan** agar histori tetap aman.

Tidak ada penghapusan paksa terhadap histori transaksi.

## Numeric / Stok
- Input angka bulat menggunakan langkah 1.
- `1` tetap `1`, `2` tetap `2`, `10` tetap `10`.
- Tampilan stok seperti `24.000` dinormalisasi menjadi **24**.
- Nilai database tidak dikalikan 1.000.
- Nilai pecahan yang benar tetap dipertahankan.
- Normalisasi hanya memengaruhi representasi UI, bukan nilai database.

## CRUD dan kontrol data
- **Produk:** Tambah, Edit, Nonaktifkan, Hapus aman.
- **Kategori:** Tambah, Edit, Simpan, Hapus.
- **Satuan:** Tambah, Edit, Simpan, Hapus.
- **Supplier:** Tambah, Edit, Simpan, Hapus.
- **Pelanggan:** Tambah, Edit, Simpan, Hapus.
- Master data dapat dipilih dengan klik baris tabel.
- Master yang masih direferensikan dilindungi dari penghapusan.
- **Stok & Mutasi:** koreksi dilakukan sebagai mutasi baru, bukan menghapus histori.
- **Pembelian/Kas:** koreksi transaksi menggunakan mekanisme yang menjaga histori.
- **Dashboard/Laporan:** read-only.
- **Pengaturan/Printer:** edit dan simpan konfigurasi.
- **Backup/Restore:** action-based.

## Kasir
Workflow Kasir yang sudah tersedia:
- Cari Produk berdasarkan nama/barcode.
- Scan barcode dan Enter.
- Qty − / + dengan validasi stok.
- Hapus item.
- Batal transaksi.
- Riwayat hingga 100 transaksi.
- Cetak ulang struk.
- Parkir transaksi sementara selama sesi aplikasi.
- Daftar parkiran untuk lanjutkan/hapus.
- Shortcut F4 bayar, F8 riwayat, F9 parkiran, F10 parkir, Esc batal.

**Menu Kasir untuk sementara dibekukan pada tahap audit saat ini.** Pengembangan berikutnya tidak dilakukan sampai diminta.

## Reset Data
Tersedia pada Backup / Restore untuk ADMIN:
- **RESET TRANSAKSI & STOK** — membersihkan transaksi, pembelian, mutasi dan mengosongkan stok tanpa menghapus master bisnis.
- **RESET SEMUA DATA BISNIS** — membersihkan seluruh master bisnis dan histori bisnis tanpa menghapus user/settings.
- Konfirmasi dua tahap dan wajib mengetik `RESET`.
- Backup tetap disarankan sebelum reset.

## Integritas transaksi
- Invoice unik.
- Barcode unik.
- Stok tidak boleh negatif.
- Penjualan atomic.
- CASH menambah kas; QRIS/TRANSFER/DEBIT tidak menambah kas.
- Pembayaran non-tunai harus sama dengan total.
- Kembalian hanya CASH.
- Mutasi stok dicatat untuk penjualan, pembelian dan penyesuaian.
- Nilai Decimal non-finite ditolak.
- Service melakukan rollback pada kegagalan commit.

## Keamanan
- Password PBKDF2-SHA256 dengan salt acak.
- User inactive tidak dapat login.
- Minimal satu Administrator aktif.
- Mutation user memiliki rollback protection.

## Default login
- Username: `admin`
- Password: `admin123`

## Data Windows
Database dan backup EXE berada di `%LOCALAPPDATA%\\WPOS PRO 2`.

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

## Tema
- **Dark Mode** — default.
- **Light Mode**.
- Modern Blue, Purple Premium, Emerald, Kemerdekaan dan Keagamaan telah dihapus.
- Key tema invalid/lama fallback ke DARK.

## UI
- Sidebar text-only tanpa ikon menu.
- Sidebar section background untuk OPERASIONAL, KEUANGAN, DATA MASTER dan SYSTEM.
- Form Produk, Pembelian, Supplier dan Pelanggan menggunakan popup hybrid.
- Kategori dan Satuan menggunakan form inline/horizontal.
- Clear button `×` dikendalikan oleh global UI.
- Footer: **Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana**.

## Excel Produk
- Export `.xlsx`.
- Template `.xlsx`.
- Import mode Tambah atau Update berdasarkan Barcode.
- Update tidak mengubah stok berjalan.
- Import tidak mengubah transaksi atau saldo kas.

## Versioning
- Fitur/perubahan besar: naik MINOR.
- Perbaikan/perubahan kecil: naik PATCH.
- Setiap perubahan source, config, installer, test atau dokumentasi dicatat di README.

## Changelog
### 2.7.1
- Memperbaiki tampilan stok pada menu Produk agar `24.000` tampil sebagai `24`.
- Normalisasi stok dilakukan pada lapisan UI dan tidak mengalikan nilai database.
- Normalisasi tetap diterapkan setelah tabel Produk di-refresh.
- Menambahkan **Hapus Produk** permanen.
- Penghapusan hanya diizinkan untuk produk tanpa histori penjualan, pembelian dan mutasi stok.
- Produk yang sudah memiliki histori tetap dilindungi dan harus menggunakan **Nonaktifkan**.
- Menambahkan service penghapusan produk dengan rollback protection.
- Menambahkan sinkronisasi versi config dan installer ke **2.7.1**.

### 2.7.0
- Menambahkan Parkir Transaksi dan Daftar Parkiran pada Kasir.
- Menambahkan shortcut F9 dan F10.
- Parkiran tidak membuat transaksi penjualan, mutasi stok atau mutasi kas sampai checkout.
- Tidak mengubah schema database Kasir pada tahap ini.

### 2.6.0
- Menyempurnakan workflow Kasir satu komputer.
- Pencarian produk nama/barcode.
- Qty − / + dengan validasi stok.
- Hapus Item dan Batal Transaksi.
- Riwayat transaksi dan Cetak Ulang Struk.
- Shortcut F4, F8 dan Escape.

### 2.5.1
- Struktur sidebar OPERASIONAL, KEUANGAN, DATA MASTER dan SYSTEM.
- Background section theme-aware.
- SYSTEM memiliki jarak visual lebih besar.
- Sidebar tetap text-only.

### 2.5.0
- Reset Transaksi & Stok.
- Reset Semua Data Bisnis.
- Konfirmasi dua tahap dengan kata `RESET`.
- User dan settings dipertahankan.

## Arsitektur utama
- `app/ui/modern_main_window.py` — shell/sidebar/topbar/stack.
- `app/ui/main_window.py` — halaman dan workflow.
- `app/ui/premium_cashier.py` — UI Kasir.
- `app/ui/master_data.py` — CRUD master data.
- `app/ui/form_layouts.py` — hybrid form, Excel UI, normalisasi stok Produk dan kontrol reset/hapus Produk.
- `app/ui/global_ui.py` — aturan global kontrol/geometry.
- `app/ui/theme_shell.py` — palette DARK/LIGHT.
- `app/ui/ux2026.py` — interaction/accessibility.
- `app/services/product_delete.py` — penghapusan produk aman berbasis histori.
- `app/services/reset.py` — reset data bisnis dengan FK-safe deletion.
