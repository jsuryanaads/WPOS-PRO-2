# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.3.10**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## 14 halaman aplikasi
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

## Alur kasir
Barcode → Keranjang → Diskon → Pembayaran → Kembalian → Stok berkurang → Transaksi tersimpan → Cetak struk.

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

Hasil build:
`dist\\WPOS PRO 2\\WPOS PRO 2.exe`

## Installer
Compile `installer.iss` menggunakan Inno Setup.

Hasil installer:
`installer\\WPOS_PRO_2_Setup.exe`

## Tema aplikasi
Dua tema resmi tersedia:
- **Dark Mode** — tema default.
- **Light Mode** — tema terang; sidebar, navigasi, brand/account panel, hover dan logout mengikuti palette Light Mode.

Tema yang sudah dihapus dan tidak tersedia:
- Modern Blue
- Purple Premium
- Emerald
- Kemerdekaan
- Keagamaan

Key tema lama atau tidak valid yang tersimpan di database otomatis fallback ke **DARK**.

## Dashboard Welcome Header
Header Dashboard sekarang memakai topbar modern sebagai satu-satunya area sambutan:
- **Selamat datang, {username login}**.
- Tanggal menggunakan tanggal komputer saat aplikasi berjalan.
- Nama hari ditampilkan dalam Bahasa Indonesia.
- Header lama/branding internal Dashboard disembunyikan agar tidak ada ruang kosong atau header ganda.
- Kompatibel dengan Dark Mode dan Light Mode.

## Dashboard KPI
- **TRANSAKSI HARI INI** hanya menghitung transaksi pada hari kalender lokal saat aplikasi dibuka.
- **OMZET HARI INI** hanya menghitung omzet pada hari kalender lokal saat aplikasi dibuka.
- **PRODUK AKTIF** tetap menghitung seluruh produk aktif.
- **STOK MENIPIS / HABIS** tetap merupakan kondisi stok saat ini.
- **SALDO KAS** tetap saldo berjalan dan tidak dibatasi hanya hari ini.

## Kasir
Halaman Kasir menggunakan workflow fokus transaksi:
- Input barcode di bagian atas dengan Enter untuk menambah barang.
- Keranjang mengambil ruang utama agar daftar item mudah dipantau.
- Ringkasan pembayaran memakai panel kanan dengan lebar minimum yang cukup untuk label dan field nominal.
- Tombol **CLEAR** dan **BAYAR & CETAK** memiliki ukuran minimum agar teks tidak terpotong atau berhimpitan pada resolusi desktop.
- Metode pembayaran tetap **CASH, QRIS, TRANSFER, DEBIT**.
- Perubahan ini hanya memperbaiki geometry/presentasi UI dan tidak mengubah business logic pembayaran, stok, transaksi atau database schema.

## Form input — Hybrid UX
Pada **v2.3.4**, form input menggunakan pola hybrid agar halaman data tidak dipenuhi form panjang:
- **Produk:** form lengkap dibuka sebagai popup; tabel produk tetap menjadi fokus halaman.
- **Pembelian:** form lengkap dibuka sebagai popup; ruang halaman tetap lebih lega.
- **Supplier:** form lengkap dibuka sebagai popup.
- **Pelanggan:** form lengkap dibuka sebagai popup.
- **Kategori:** form satu field tetap inline/horizontal.
- **Satuan:** form satu field tetap inline/horizontal.
- **Stok & Mutasi:** tetap inline/horizontal untuk input cepat.
- **Kas:** tetap inline/horizontal untuk transaksi cepat.
- **Pengaturan Toko** dan **Printer:** tetap menggunakan form horizontal/compact.
- **Backup / Restore:** tetap berupa action buttons, bukan popup form data.

Lapisan `app/ui/form_layouts.py` hanya mengubah penyajian dan penempatan widget. Widget serta signal bisnis yang sudah ada dipertahankan; tidak ada perubahan business logic atau database schema.

## Footer aplikasi
Struktur bersama:
**Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana**

Spesifikasi:
- Tinggi tetap **30 px**.
- Teks **10 px**.
- Login dan modern shell memakai helper `add_application_footer()`.
- Footer modern berada di luar `QStackedWidget`.

## Audit UI
Audit v2.2.0 mencakup seluruh 14 halaman dengan normalisasi spacing, margin, form, groupbox, tabel, scrollbar, field input, tombol, header dan master pages tanpa mengubah business logic atau database schema.

## Versioning
- **Perubahan besar / fitur besar:** naik **MINOR**, contoh `2.2.0` → `2.3.0`.
- **Perbaikan / perubahan kecil:** naik **PATCH**, contoh `2.2.0` → `2.2.1`.
- Setiap perubahan source, konfigurasi, build, CI atau dokumentasi wajib dicatat di README dan menggunakan kenaikan versi yang sesuai.

## Changelog
### 2.3.10
- Memperbaiki kasus tombol **×** yang masih muncul pada `QDoubleSpinBox`/`QSpinBox` setelah clear button global pada `QLineEdit` dihapus.
- Menonaktifkan clear button secara eksplisit pada `QLineEdit` internal milik seluruh numeric spinbox.
- Menambahkan marker internal `wposClearButtonDisabled` untuk memastikan kontrak UI tersebut dapat diaudit.
- Menambahkan regression test khusus numeric spinbox.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.10**.
- Tidak mengubah business logic, transaksi, stok, pembayaran atau database schema.

### 2.3.9
- Menghapus aktivasi global tombol clear **×** pada seluruh `QLineEdit` agar tombol tersebut tidak muncul otomatis di setiap halaman.
- Mempertahankan normalisasi tinggi dan fokus field input serta geometry spinner.
- Menambahkan regression test untuk memastikan global UI tidak mengaktifkan clear button.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.9**.
- Tidak mengubah business logic, transaksi, stok, pembayaran atau database schema.

### 2.3.8
- Memperbaiki geometry halaman **Kasir** berdasarkan audit screenshot produksi.
- Memperlebar panel **Ringkasan Pembayaran** agar field Diskon, Metode dan Bayar tidak terlalu sempit.
- Memberi ukuran minimum pada tombol **CLEAR** dan **BAYAR & CETAK** agar teks dan target klik tetap jelas.
- Mengurangi ketergantungan pada rasio stretch sehingga panel pembayaran tetap stabil pada resolusi desktop.
- Menambahkan regression test untuk geometry panel pembayaran dan keberadaan seluruh metode pembayaran.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.8**.
- Tidak mengubah business logic transaksi atau database schema.

### 2.3.7
- Memperbaiki tampilan Dashboard berdasarkan audit screenshot produksi.
- Menghilangkan header/branding Dashboard internal yang sebelumnya menyisakan area kosong dan logo terpisah.
- Memusatkan informasi sambutan pada topbar modern: **Selamat datang, {username}** dan tanggal aktual Bahasa Indonesia.
- Mempertahankan KPI harian dan saldo kas berjalan dari v2.3.6.
- Menambahkan regression coverage untuk penggunaan topbar modern dan penyembunyian legacy header.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.7**.
- Tidak mengubah business logic transaksi atau database schema.

### 2.3.6
- Memperbaiki Dashboard agar **TRANSAKSI** dan **OMZET** benar-benar menggunakan rentang hari kalender lokal saat ini.
- Memisahkan semantik **SALDO KAS** sebagai saldo berjalan sehingga tidak ikut difilter ke hari ini.
- Mengubah welcome header dari teks statis menjadi username login yang aktual.
- Mengubah tanggal welcome header menjadi tanggal komputer aktual dengan nama hari Bahasa Indonesia.
- Memperbarui regression test agar tidak bergantung pada tanggal statis.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.6**.
- Tidak mengubah business logic transaksi atau database schema.

### 2.3.5
- Memperbaiki deteksi container `QGroupBox` pada lapisan hybrid form sehingga popup Produk dan Pembelian benar-benar terpasang pada form produksi.
- Menjaga mode popup/inline tetap hanya sebagai perubahan presentasi UI.
- Menambahkan regression coverage yang sesuai dengan indeks 14 halaman produksi.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.5**.
- Tidak mengubah business logic atau database schema.

### 2.3.4
- Menerapkan **hybrid form UX** pada 14 halaman sesuai karakter input.
- Produk dan Pembelian menggunakan popup untuk form kompleks.
- Supplier dan Pelanggan menggunakan popup untuk form multi-field.
- Kategori dan Satuan menggunakan form inline/horizontal satu field.
- Stok & Mutasi, Kas, Pengaturan Toko dan Printer mempertahankan pola input cepat/horizontal yang sesuai.
- Menambahkan `app/ui/form_layouts.py` sebagai lapisan presentasi tanpa mengubah business logic.
- Menambahkan regression test untuk mode popup dan inline.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.4**.
- Tidak mengubah business logic atau database schema.

### 2.3.3
- Mengganti branding strip Dashboard dengan **Selamat datang, Admin**.
- Menampilkan **Senin, 12 September 2026** sebagai tanggal pada header sambutan sesuai permintaan desain.
- Menjaga header tetap kompatibel dengan Dark Mode dan Light Mode.
- Menambahkan regression test untuk Dashboard Welcome Header.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.3**.
- Tidak mengubah business logic atau database schema.

### 2.3.2
- Memperbaiki Light Mode agar sidebar modern tidak lagi mempertahankan warna gelap.
- Sidebar, navigasi, brand/account panel, hover dan logout mengikuti palette Light Mode.
- Menambahkan warna khusus `sidebar_text` dan `sidebar_inverse`.
- Menambahkan regression test untuk stylesheet sidebar Light Mode.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.2**.
- Tidak mengubah business logic atau database schema.

### 2.3.1
- Menambahkan Light Mode sebagai tema resmi baru.
- Mempertahankan Dark Mode sebagai tema default.
- Menghapus Modern Blue, Purple Premium dan Emerald tetap berlaku.
- Menambahkan palette Light Mode pada registry tema dan shell modern.
- Menambahkan fallback tema tidak valid ke DARK tanpa mengubah schema database.
- Memperbarui regression test untuk registry tema DARK dan LIGHT.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.1**.
- Tidak mengubah business logic atau database schema.

### 2.3.0
- Menetapkan Dark Mode sebagai satu-satunya tema resmi sementara.
- Menghapus Modern Blue, Purple Premium dan Emerald dari registry tema.
- Mengubah fallback tema database menjadi DARK.

### 2.2.0
- Audit dan normalisasi layout seluruh 14 halaman.
- Menetapkan kontrak geometry/UX global untuk form, tabel, tombol dan scrollbar.
- Menghilangkan duplikasi header halaman pada modern shell.
- Menyamakan geometry master pages Kategori, Satuan, Supplier dan Pelanggan.
- Menyamakan identitas window dengan `APP_NAME`.
- Tidak mengubah business logic atau database schema.

### 2.1.1
- Memperbaiki branding Dashboard agar seluruh identitas mengikuti WPOS PRO 2.
- Menyamakan judul window dengan `APP_NAME`.
- Menambahkan empty-state Dashboard.

### 2.0.7
- Menyatukan footer Login dan modern shell menggunakan `add_application_footer()`.

### 2.0.0
- Standardisasi identitas aplikasi menjadi WPOS PRO 2.
- Sinkronisasi nama aplikasi, data directory, EXE, installer dan branding.

## Status
**WPOS PRO 2 — v2.3.10.** Perbaikan clear button pada QLineEdit dan numeric spinbox sudah masuk source, regression test ditambahkan, dan CI harus PASS sebelum build EXE/installer dianggap release final.
