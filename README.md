# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.7.8**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Perubahan terbaru 2.7.8
- Headerbar final menggunakan tiga zona: **Context | Nama Toko | Pengguna + Tanggal**.
- Kiri: nama halaman aktif dan subtitle/hint.
- Tengah: **Nama Toko** yang dibaca dari `Pengaturan Toko` (`store_name`).
- Kanan: `Selamat datang, [username]` dan tanggal otomatis dua baris dengan hari dalam bahasa Indonesia.
- Contoh tanggal: `12 September 2026` / `Sabtu`.
- Nama toko menggunakan fallback `TOKO SEMBAKO` jika pengaturan belum tersedia.
- Perubahan hanya pada presentation layer; database dan business logic transaksi tidak diubah.

## Perubahan terbaru 2.7.7
- Menata ulang **struktur Kasir PRO** agar alur kerja kasir lebih jelas.
- Area **Input Produk** tetap menjadi area paling atas untuk barcode, Qty, Tambah dan Cari Produk.
- **Keranjang Transaksi** menjadi area kerja utama dan lebih dominan.
- Panel **Pembayaran** dipertahankan ringkas di sisi kanan dengan lebar 290–330 px.
- Panel pembayaran difokuskan pada Total, Diskon, Metode, Bayar dan Kembalian.
- Kontrol **Parkir, Transaksi Parkir, Batal Transaksi, Riwayat dan Bayar & Cetak** dipisahkan menjadi area **Kontrol Transaksi** di bawah keranjang.
- Struktur baru hanya mengatur tampilan dan penempatan widget; signal, workflow checkout, database dan business logic tetap menggunakan implementasi yang sudah ada.
- Tidak ada perubahan schema database.

## Perubahan terbaru 2.7.6
- Merapikan struktur Headerbar menjadi tiga zona yang jelas.
- Kiri: nama halaman aktif + subtitle/hint.
- Tengah: informasi pengguna.
- Kanan: tanggal otomatis.
- Status `OFFLINE` dan `DATABASE LOKAL` dihapus dari Headerbar.
- Tinggi Headerbar dijaga ringkas pada kisaran 58–64 px.

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
- Section header dirender sebagai item teks disabled yang stabil.
- Lebar sidebar: **230 px**.
- Row menu compact dan konsisten; scroll horizontal dinonaktifkan.
- Active menu, hover, section header dan spacing mengikuti tema aktif.
- Index navigasi halaman tidak berubah.

## Struktur Headerbar FINAL
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ KASIR                    TOKO SEMBAKO SAPNI        Selamat datang, Admin    │
│ Transaksi cepat · barcode first                    12 September 2026        │
│                                                     Sabtu                    │
└─────────────────────────────────────────────────────────────────────────────┘
```
- **Kiri — Context:** nama halaman aktif + subtitle/hint.
- **Tengah — Nama Toko:** membaca `store_name` dari Pengaturan Toko.
- **Kanan — Pengguna + Tanggal:** `Selamat datang, [username]`, tanggal otomatis, dan nama hari.
- Format tanggal Indonesia: `12 September 2026`.
- Hari Indonesia: `Senin` sampai `Minggu`.
- Status `OFFLINE` dan `DATABASE LOKAL` tidak ditampilkan di Headerbar.
- Headerbar ringkas dan konsisten pada Dark Mode dan Light Mode.

## Struktur Kasir PRO
- **Input Produk:** Barcode / Cari Produk, Qty, Tambah dan Cari Produk.
- **Keranjang Transaksi:** tabel Barcode, Produk, Qty, Harga dan Subtotal.
- **Kontrol keranjang:** `− QTY`, `+ QTY`, `HAPUS ITEM`.
- **Pembayaran:** Total, Diskon, Metode Pembayaran, Bayar dan Kembalian.
- **Kontrol Transaksi:** Parkir, Transaksi Parkir, Batal Transaksi, Riwayat Transaksi dan Bayar & Cetak.
- Keranjang menjadi area utama transaksi; pembayaran tetap menjadi panel kanan yang ringkas.
- Penempatan ulang kontrol tidak mengubah callback, service transaksi atau aturan pembayaran.

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
- Headerbar tiga zona: Context kiri, Nama Toko di tengah, Pengguna + Tanggal di kanan.
- Nama Toko Headerbar mengambil `store_name` dari Pengaturan Toko.
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
### 2.7.8
- Menambahkan `app/ui/headerbar.py` sebagai presentation layer Headerbar.
- Mengubah zona tengah Headerbar dari welcome text menjadi **Nama Toko**.
- Nama Toko dibaca dari `Pengaturan Toko` melalui key `store_name`.
- Zona kanan menampilkan `Selamat datang, [username]` dan tanggal dua baris dengan nama hari otomatis.
- Menambahkan fallback `TOKO SEMBAKO` jika pengaturan toko belum tersedia.
- Menambahkan styling `modernStoreName` dan memperjelas area tanggal.
- Menyinkronkan config dan installer ke **2.7.8**.

### 2.7.7
- Menambahkan modul `app/ui/cashier_structure.py` untuk merapikan hierarki visual Kasir.
- Menjadikan Keranjang Transaksi sebagai area kerja utama.
- Membatasi panel Pembayaran pada 290–330 px.
- Memindahkan kontrol Parkir, Transaksi Parkir, Batal, Riwayat dan Bayar & Cetak ke area Kontrol Transaksi di bawah keranjang.
- Menjaga callback dan workflow bisnis yang sudah ada.
- Menambahkan styling khusus untuk area Kontrol Transaksi.
- Menyinkronkan config dan installer ke **2.7.7**.

### 2.7.6
- Menata ulang Headerbar menjadi tiga zona: Context, Informasi Pengguna, dan Tanggal.
- Menampilkan nama halaman aktif dan subtitle/hint di kiri.
- Menampilkan informasi pengguna di tengah.
- Menampilkan tanggal otomatis bahasa Indonesia di kanan.
- Menghapus badge status `OFFLINE` dan `DATABASE LOKAL` dari Headerbar.
- Menetapkan tinggi Headerbar 58–64 px.

### 2.7.5
- Memperbaiki header section sidebar yang sebelumnya tampil sebagai bar kosong.
- Mengubah header section menjadi `QListWidgetItem` disabled dengan teks langsung agar stabil di Qt.
- Mengcompact tinggi item navigasi dan menetapkan sidebar 230 px.
- Menjaga navigasi 14 halaman, active-state dan text-only UI.
- Memperlebar dan menyeimbangkan area Keranjang Belanja Kasir.
- Membatasi panel pembayaran agar keranjang menjadi area utama transaksi.
- Menambahkan helper presentasi receipt untuk menghilangkan `.0` pada Qty bilangan bulat.
- Menjaga nilai transaksi/database tetap Decimal.

### 2.7.4
- Penyempurnaan visual sidebar.
- Lebar sidebar 225–240 px agar lebih proporsional.
- Padding/margin item navigasi dirapikan.
- Active-state menu dibuat lebih tegas dan konsisten.
- Section header dan spacing antar kelompok diperbaiki.

### 2.7.3
- Memperbaiki Kembalian Kasir agar live saat nominal Bayar berubah.
- Menambahkan koneksi `valueChanged` pada field Bayar.
- Menjaga aturan pembayaran CASH/non-CASH yang sudah ada.

### 2.7.2
- Memperbaiki crash login/UI akibat `form_layouts.py` mengakses `load_products` pada widget halaman yang tidak memiliki method tersebut.
- Menjadikan akses helper Produk menggunakan owner `MainWindow` secara aman.

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
- `app/ui/premium_cashier.py` — UI Kasir dasar dan workflow.
- `app/ui/cashier_structure.py` — struktur presentasi Kasir dan kontrol transaksi.
- `app/ui/headerbar.py` — struktur presentasi Headerbar dan nama toko/tanggal.
- `app/ui/master_data.py` — CRUD master data.
- `app/ui/form_layouts.py` — hybrid form, Excel UI, reset dan kontrol Produk.
- `app/ui/global_ui.py` — aturan global kontrol/geometry.
- `app/ui/theme_shell.py` — palette DARK/LIGHT dan styling sidebar/Kasir/Headerbar.
- `app/ui/ux2026.py` — interaction/accessibility.
- `app/services/product_delete.py` — penghapusan Produk dengan perlindungan histori.
- `app/services/receipt_display.py` — normalisasi presentasi Qty pada struk.
