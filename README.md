# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.7.5**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Perubahan terbaru 2.7.5
- Memperbaiki **sidebar** agar seluruh kelompok menu tampil normal dan tidak berubah menjadi bar kosong.
- Header sidebar **OPERASIONAL, KEUANGAN, DATA MASTER dan SYSTEM** sekarang dirender sebagai item teks yang stabil.
- Sidebar dibuat compact dengan lebar tetap **230 px** dan tinggi baris yang konsisten agar 14 halaman lebih mudah terlihat pada resolusi Windows umum.
- Scroll horizontal sidebar dinonaktifkan; scroll vertikal hanya muncul jika memang diperlukan.
- Active menu tetap jelas tanpa ikon dekoratif dan index navigasi tidak berubah.
- Memperlebar area **Keranjang Belanja** pada Kasir agar lebih dominan dibanding panel pembayaran.
- Panel pembayaran dibatasi agar tidak mengambil ruang berlebihan pada layar lebar.
- Tampilan Qty pada struk Qt/HTML dinormalisasi: `1.0`, `2.0`, `3.0` menjadi `1`, `2`, `3`.
- Perubahan Qty hanya presentasi struk; nilai Decimal dan perhitungan transaksi tetap tidak diubah.

## Perubahan terbaru 2.7.4
- Merapikan **menu sidebar** tanpa mengubah fungsi atau index navigasi.
- Sidebar tetap text-only tanpa ikon dekoratif.
- Lebar sidebar dibuat lebih proporsional agar area kerja utama lebih luas.
- Item menu dibuat lebih rapi dengan padding, margin dan active-state yang konsisten.
- Header kelompok OPERASIONAL, KEUANGAN, DATA MASTER dan SYSTEM dibuat lebih jelas.
- Jarak antar kelompok diperbaiki, termasuk pemisahan area SYSTEM.
- Styling tetap mengikuti Dark Mode dan Light Mode.
- Tidak ada perubahan database atau business logic.

## Perubahan terbaru 2.7.3
- Memperbaiki **Kembalian** pada Kasir agar berubah langsung ketika nominal **Bayar** diketik/diubah.
- Pembaruan menggunakan signal `valueChanged` pada field Bayar dan tidak mengubah aturan pembayaran pada service transaksi.
- CASH tetap menghitung kembalian; pembayaran non-CASH tetap tidak menghasilkan kembalian.
- Perubahan hanya pada workflow/UI pembayaran Kasir.

## Perubahan 2.7.2
- Memperbaiki crash login ketika `apply_hybrid_form_layouts()` memproses halaman Produk.
- Helper Produk menggunakan owner `MainWindow` untuk mengakses `load_products` dan aksi Produk.
- Fitur Hapus Produk tetap tersedia dengan perlindungan histori.

## Role
Role resmi aplikasi:
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

## Struktur sidebar
- **OPERASIONAL:** Dashboard, Kasir, Produk, Stok & Mutasi, Pembelian.
- **KEUANGAN:** Kas, Laporan.
- **DATA MASTER:** Pelanggan, Supplier, Kategori, Satuan.
- **SYSTEM:** Pengaturan Toko, Printer, Backup / Restore.
- Sidebar text-only tanpa ikon dekoratif.
- Section header dirender sebagai item teks disabled yang stabil, bukan custom widget yang dapat berubah menjadi bar kosong.
- Lebar sidebar: **230 px**.
- Row menu compact dan konsisten; scroll horizontal dinonaktifkan.
- Active menu, hover, section header dan spacing mengikuti tema aktif.
- Index navigasi halaman tidak berubah.

## CRUD dan kontrol data
- **Produk:** Tambah, Edit, Simpan, Nonaktifkan, Hapus aman.
- Produk yang sudah memiliki histori transaksi/mutasi ditolak untuk penghapusan permanen; gunakan **Nonaktifkan**.
- **Kategori:** Tambah, Edit, Simpan, Hapus.
- **Satuan:** Tambah, Edit, Simpan, Hapus.
- **Supplier:** Tambah, Edit, Simpan, Hapus.
- **Pelanggan:** Tambah, Edit, Simpan, Hapus.

## Kasir
- Cari Produk berdasarkan nama/barcode.
- Scanner barcode + Enter.
- Qty − / +.
- Hapus item dan batal transaksi dengan konfirmasi.
- Diskon transaksi.
- **Bayar dan Kembalian live:** nominal Bayar CASH langsung memperbarui Kembalian.
- Pembayaran non-CASH otomatis mengikuti total transaksi dan kembalian tetap Rp 0.
- Riwayat transaksi dan cetak ulang struk.
- Parkir transaksi selama sesi aplikasi.
- Area Keranjang Belanja dibuat lebih lebar daripada panel pembayaran.
- Qty bilangan bulat pada struk ditampilkan tanpa suffix `.0`.
- Shortcut F4, F8, F9, F10 dan Escape.

## Reset Data
- **RESET TRANSAKSI & STOK** mempertahankan master bisnis.
- **RESET SEMUA DATA BISNIS** membersihkan master bisnis dan transaksi.
- User dan pengaturan toko dipertahankan.
- Konfirmasi dua tahap dan wajib mengetik `RESET`.

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

## Tema
- **Dark Mode** — default.
- **Light Mode**.
- Tema lama yang tidak digunakan sudah dihapus dan key invalid fallback ke DARK.

## Numeric Input
- Input desktop angka bulat menggunakan langkah 1.
- `1` tetap `1`, `2` tetap `2`, `10` tetap `10`.
- Tampilan stok bulat seperti `24.000` dinormalisasi menjadi `24` tanpa mengubah database.
- Nilai pecahan yang benar tetap dipertahankan.
- Tidak ada faktor ×1.000.

## UI
- Sidebar navigasi text-only tanpa ikon menu.
- Section sidebar: OPERASIONAL, KEUANGAN, DATA MASTER, SYSTEM.
- Sidebar compact 230 px dengan header teks stabil.
- Active menu dan hover dibuat konsisten pada Dark/Light Mode.
- Form Produk, Pembelian, Supplier dan Pelanggan menggunakan popup hybrid.
- Kategori dan Satuan menggunakan form inline/horizontal.
- Clear button `×` dikendalikan oleh global UI.
- Footer: **Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana**.

## Excel Produk
- Export `.xlsx`.
- Template `.xlsx`.
- Import mode Tambah atau Update berdasarkan Barcode.
- Update tidak mengubah stok berjalan.

## Versioning
- Fitur/perubahan besar: naik MINOR.
- Perbaikan/perubahan kecil: naik PATCH.
- Setiap perubahan source, config, installer, test atau dokumentasi dicatat di README.

## Changelog
### 2.7.5
- Memperbaiki header section sidebar yang sebelumnya tampil sebagai bar kosong.
- Mengubah header section menjadi `QListWidgetItem` disabled dengan teks langsung agar stabil di Qt.
- Mengcompact tinggi item navigasi dan menetapkan sidebar 230 px.
- Menjaga navigasi 14 halaman, active-state dan text-only UI.
- Memperlebar dan menyeimbangkan area Keranjang Belanja Kasir.
- Membatasi panel pembayaran agar keranjang menjadi area utama transaksi.
- Menambahkan helper presentasi receipt untuk menghilangkan `.0` pada Qty bilangan bulat.
- Menjaga nilai transaksi/database tetap Decimal.
- Menyinkronkan config dan installer ke **2.7.5**.

### 2.7.4
- Penyempurnaan visual sidebar.
- Lebar sidebar 225–240 px agar lebih proporsional.
- Padding/margin item navigasi dirapikan.
- Active-state menu dibuat lebih tegas dan konsisten.
- Section header dan spacing antar kelompok diperbaiki.
- Menyinkronkan config dan installer ke **2.7.4**.

### 2.7.3
- Memperbaiki Kembalian Kasir agar live saat nominal Bayar berubah.
- Menambahkan koneksi `valueChanged` pada field Bayar setelah Premium Cashier dibangun.
- Menjaga aturan pembayaran CASH/non-CASH yang sudah ada.
- Menyinkronkan config dan installer ke **2.7.3**.

### 2.7.2
- Memperbaiki crash login/UI akibat `form_layouts.py` mengakses `load_products` pada widget halaman yang tidak memiliki method tersebut.
- Menjadikan akses helper Produk menggunakan owner `MainWindow` secara aman.
- Mempertahankan Hapus Produk dan normalisasi tampilan stok.
- Menyinkronkan config dan installer ke **2.7.2**.

### 2.7.1
- Menambahkan Hapus Produk permanen dengan konfirmasi.
- Produk yang memiliki histori penjualan, pembelian atau mutasi stok tidak dapat dihapus permanen.
- Menambahkan normalisasi tampilan stok agar angka bulat tidak tampil sebagai `24.000`.

### 2.7.0
- Pengembangan workflow Kasir PRO dan Parkir Transaksi.

### 2.6.0
- Menyempurnakan workflow Kasir: pencarian produk, Qty, hapus item, batal transaksi, riwayat, cetak ulang dan shortcut.

### 2.5.1
- Memperjelas section sidebar dan styling Dark/Light Mode.

### 2.5.0
- Menambahkan Reset Data dengan konfirmasi dua tahap.

## Arsitektur
- `app/ui/modern_main_window.py` — shell/sidebar/topbar/stack.
- `app/ui/main_window.py` — halaman dan workflow.
- `app/ui/premium_cashier.py` — UI Kasir.
- `app/ui/master_data.py` — CRUD master data.
- `app/ui/form_layouts.py` — hybrid form, Excel UI, reset dan kontrol Produk.
- `app/ui/global_ui.py` — aturan global kontrol/geometry.
- `app/ui/theme_shell.py` — palette DARK/LIGHT dan styling sidebar/Kasir.
- `app/ui/ux2026.py` — interaction/accessibility.
- `app/services/product_delete.py` — penghapusan Produk dengan perlindungan histori.
- `app/services/receipt_display.py` — normalisasi presentasi Qty pada struk.
