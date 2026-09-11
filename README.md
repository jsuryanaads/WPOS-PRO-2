# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.4.2**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Role & Administrasi
Role resmi aplikasi hanya:
- **ADMIN** — akses penuh dan fungsi administrasi.
- **KASIR** — akses operasional kasir terbatas.

Role **PENGELOLA** dan **TEKNISI** telah dihapus dari role policy dan tidak lagi dapat dibuat atau memperoleh akses melalui permission system. Database `users` dan field `role` tetap dipertahankan agar cleanup tidak merusak schema/data transaksi.

Aturan keamanan Administrator tetap berlaku: minimal satu Administrator aktif harus tersedia dan Administrator tidak boleh menonaktifkan akun sendiri.

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
- Nilai numerik bisnis yang diterima service harus finite; NaN dan Infinity ditolak.
- Kegagalan commit pada mutation service di-rollback agar session tidak tertinggal dalam keadaan parsial.

## Keamanan
- Password menggunakan PBKDF2-SHA256 dengan salt acak.
- User inactive tidak dapat login.
- Minimal satu Administrator aktif dipertahankan.
- Mutation user memiliki rollback protection.
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
Header Dashboard memakai topbar modern sebagai satu-satunya area sambutan:
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
- Clear button pada `QLineEdit`, `QSpinBox` dan `QDoubleSpinBox` dinonaktifkan agar tombol **×** tidak muncul otomatis pada field input.
- Kebijakan clear button dikendalikan oleh `global_ui.py`; layer UX tidak boleh mengaktifkannya kembali.
- Perubahan UI tidak mengubah business logic pembayaran, stok, transaksi atau database schema.

## Numeric Input / Stok / Quantity
- Seluruh numeric input desktop sekarang diperlakukan sebagai **angka bulat** untuk menghilangkan ambiguitas separator lokal.
- `1` tetap **1**, `2` tetap **2**, `10` tetap **10**.
- Tidak ada lagi tampilan `1.000`, `2.000` atau `10.000` pada field input yang dapat disalahartikan sebagai seribu, dua ribu atau sepuluh ribu.
- Input stok, minimum stok, quantity kasir, quantity pembelian, harga, diskon, pembayaran dan nominal kas menggunakan langkah **1** pada UI.
- Tidak ada faktor pengali **×1.000** pada UI maupun business service.
- Business service tetap menerima nilai dari `.value()` dan melakukan validasi Decimal; perubahan ini hanya memperjelas kontrak input desktop.
- Data database yang sudah tersimpan tidak dimigrasikan atau dikalikan otomatis.

## Sidebar navigation
Navigasi sidebar menggunakan **teks saja tanpa ikon menu**.
- Ikon dekoratif tidak lagi dirender.
- Index halaman dan mekanisme navigasi tetap sama.
- Penghapusan ikon hanya perubahan presentasi UI; tidak mengubah fungsi halaman atau business logic.

## Arsitektur UI
UI modern mengikuti pembagian tanggung jawab berikut:
- `modern_main_window.py` — shell aplikasi: sidebar, topbar, stack dan account/logout.
- `global_ui.py` — kontrak global geometry/UX dan kebijakan kontrol bersama.
- `theme_shell.py` — palette dan styling theme DARK/LIGHT.
- `ux2026.py` — interaction/accessibility tanpa palette dan tanpa mengubah kebijakan global control.
- `polish.py` — refinements theme-neutral yang tidak mengambil alih kontrak global.
- `main_window.py`, `premium_cashier.py`, `master_data.py` — layout dan workflow halaman.
- `form_layouts.py` — penataan form hybrid/popup dan aksi Excel Produk sebagai presentation layer.
- `dashboard_welcome.py` — welcome content Dashboard.
- `services/validation.py` — validasi Decimal terpusat untuk nilai numerik finite dan non-negative sesuai domain.
- `services/excel.py` — import/export Produk berbasis `.xlsx`.

Aturan penting: **global_ui.py adalah sumber aturan global untuk kontrol dan geometry; theme_shell.py adalah sumber palette; layer halaman tidak boleh mengaktifkan kembali aturan global yang sudah dinonaktifkan.** Business logic tetap berada di `app/services/` dan database model di `app/models.py`.

## Form input — Hybrid UX
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

## Excel Produk
Fitur Excel tersedia di halaman **Produk**:
- **Export Excel** — mengekspor seluruh data produk ke `.xlsx`.
- **Template Excel** — menghasilkan file `.xlsx` dengan format kolom yang sama untuk import massal.
- **Import Excel** — pilihan **Tambah** atau **Update berdasarkan Barcode**.
- Format kolom: `Barcode`, `Nama Produk`, `Kategori`, `Satuan`, `Harga Beli`, `Harga Jual`, `Stok Awal`, `Stok Minimum`, `Aktif`.
- Barcode harus unik, nama wajib, angka bisnis tidak boleh negatif/non-finite.
- Kategori dan Satuan harus sudah tersedia di master data.
- Import diproses **atomic**: jika ada error validasi, perubahan tidak diterapkan.
- Mode **Update** tidak mengubah stok berjalan; perubahan stok tetap melalui Stok & Mutasi.
- Produk baru dengan Stok Awal membuat `StockMovement` bertipe `OPENING` dengan referensi `IMPORT-EXCEL`.
- Import Excel tidak dapat mengubah transaksi penjualan, pembelian atau saldo kas.

## Footer aplikasi
Struktur bersama:
**Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana**

Spesifikasi:
- Tinggi tetap **30 px**.
- Teks **10 px**.
- Login dan modern shell memakai helper `add_application_footer()`.
- Footer modern berada di luar `QStackedWidget`.

## Versioning
- **Perubahan besar / fitur besar:** naik **MINOR**, contoh `2.2.0` → `2.3.0`.
- **Perbaikan / perubahan kecil:** naik **PATCH**, contoh `2.2.0` → `2.2.1`.
- Setiap perubahan source, konfigurasi, build, CI atau dokumentasi wajib dicatat di README dan menggunakan kenaikan versi yang sesuai.

## Changelog
### 2.4.2
- Memperbaiki akar masalah numeric input yang masih dapat dibaca sebagai format ribuan karena `QDoubleSpinBox` memakai presisi 3 desimal.
- Numeric input desktop sekarang menggunakan presisi **0 desimal** dan langkah **1**.
- `1` → `1`, `2` → `2`, `10` → `10`, tanpa `1.000`, `2.000` atau `10.000` pada field input.
- Berlaku konsisten pada quantity kasir, stok/mutasi, stok awal, stok minimum, quantity pembelian, harga, diskon, pembayaran dan nominal kas.
- Tidak mengalikan nilai ×1.000 dan tidak mengubah database yang sudah ada.
- Menyinkronkan `APP_VERSION` dan installer ke **2.4.2**.
- Tidak mengubah database schema atau business service transaksi.

### 2.4.1
- Memperbaiki tampilan numeric input `QDoubleSpinBox` yang sebelumnya menampilkan angka bulat seperti `1` sebagai `1.000` sehingga berpotensi disalahartikan sebagai 1.000/seribu.
- Nilai angka sekarang ditampilkan secara compact: `1` → `1`, `2` → `2`, `10` → `10`, `1.2` → `1.2`, `1000` → `1000`.
- Tidak ada faktor pengali **×1.000** dan tidak ada perubahan pada nilai yang dikirim ke business service.
- Presisi pecahan hingga 3 desimal tetap dipertahankan untuk quantity/stok yang memang membutuhkan pecahan.
- Menambahkan regression test untuk memastikan perbaikan bersifat presentation-only.
- Menyinkronkan `APP_VERSION` dan installer ke **2.4.1**.
- Tidak mengubah database schema, business logic transaksi, pembayaran, stok, kas atau alur kasir.

### 2.4.0
- Menambahkan fitur **Export Produk ke Excel** (`.xlsx`).
- Menambahkan **Template Excel Produk** untuk input massal.
- Menambahkan **Import Produk dari Excel** dengan mode Tambah atau Update berdasarkan Barcode.
- Import divalidasi sebelum mutation dan menggunakan satu transaction commit agar kegagalan tidak meninggalkan data parsial.
- Update berdasarkan Barcode tidak mengubah stok berjalan.
- Produk baru dengan Stok Awal tetap menghasilkan catatan `StockMovement`.
- Menambahkan dependency `openpyxl`.
- Menambahkan regression tests untuk export/import, format header, atomic validation dan preservasi stok.
- Menyinkronkan `APP_VERSION` dan installer ke **2.4.0**.
- Tidak mengubah database schema, alur kasir, aturan pembayaran atau saldo kas.

### 2.3.16
- **Role cleanup:** role resmi disederhanakan menjadi **ADMIN** dan **KASIR**.
- Menghapus `PENGELOLA` dan `TEKNISI` dari permission policy.
- `create_user()` tidak lagi menerima/membuat role yang sudah dihapus.
- Default role pembuatan user menjadi `KASIR`.
- Permission KASIR dibatasi ke Dashboard, Kasir dan Pelanggan.
- Menambahkan regression test untuk role yang dihapus dan permission KASIR.
- Mempertahankan tabel/field user dan aturan minimal satu Administrator aktif untuk menjaga kompatibilitas database.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.16**.
- Tidak mengubah database schema, transaksi, stok, pembayaran atau business flow.

### 2.3.15
- Hardening business-service untuk nilai Decimal: `NaN`, `Infinity` dan nilai non-finite lain sekarang ditolak secara konsisten pada produk, pembelian dan penyesuaian stok.
- Menambahkan `app/services/validation.py` sebagai validator Decimal terpusat.
- Menambahkan rollback protection pada mutation user/settings.
- Menambahkan regression tests untuk validasi finite Decimal dan rollback mutation.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.15**.

### 2.3.14
- Menemukan akar masalah tombol **×** yang kembali muncul: `ux2026.py` sebelumnya mengaktifkan `setClearButtonEnabled(True)` pada setiap `QLineEdit`, sehingga menimpa kebijakan global.
- Menghapus override tersebut dari layer UX.
- Menetapkan `global_ui.py` sebagai sumber tunggal kebijakan clear button.
- Menambahkan regression test arsitektur UI.

### 2.3.13
- Memperbaiki kasus tombol **×** pada field `QLineEdit` biasa, termasuk Pengaturan Toko.
- Menonaktifkan clear button pada seluruh `QLineEdit` dan input internal numeric spinbox.
- Menambahkan regression test global.

### 2.3.12
- Menghapus ikon dekoratif dari shell modern, termasuk ikon menu sidebar dan simbol dekoratif Dashboard.
- Mempertahankan logo WPOS sebagai identitas aplikasi.
- Menambahkan regression coverage untuk UI text-first.

### 2.3.11
- Menghapus ikon dekoratif dari seluruh menu sidebar modern.
- Sidebar hanya menampilkan nama section dan teks menu.
- Mempertahankan `Qt.UserRole` dan index navigasi.
