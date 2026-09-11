# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.3.15**
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
- `form_layouts.py` — penataan form hybrid/popup sebagai presentation layer.
- `dashboard_welcome.py` — welcome content Dashboard.
- `services/validation.py` — validasi Decimal terpusat untuk nilai numerik finite dan non-negative sesuai domain.

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
### 2.3.15
- Hardening business-service untuk nilai Decimal: `NaN`, `Infinity` dan nilai non-finite lain sekarang ditolak secara konsisten pada produk, pembelian dan penyesuaian stok.
- Menambahkan `app/services/validation.py` sebagai validator Decimal terpusat.
- Menambahkan rollback protection pada `create_user`, `set_user_active`, `reset_password` dan `set_setting` agar kegagalan commit tidak meninggalkan mutation parsial pada session.
- Menambahkan regression tests untuk validasi finite Decimal dan rollback mutation.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.15**.
- Tidak mengubah database schema, alur kasir, aturan pembayaran atau business flow.

### 2.3.14
- Menemukan akar masalah tombol **×** yang kembali muncul: `ux2026.py` sebelumnya mengaktifkan `setClearButtonEnabled(True)` pada setiap `QLineEdit`, sehingga menimpa kebijakan global.
- Menghapus override tersebut dari layer UX.
- Menetapkan `global_ui.py` sebagai sumber tunggal kebijakan clear button.
- Mempertahankan `ux2026.py` sebagai layer interaction/accessibility tanpa palette dan tanpa override kontrak global control.
- Menambahkan regression test arsitektur UI.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.14**.
- Tidak mengubah business logic atau database schema.

### 2.3.13
- Memperbaiki kasus tombol **×** pada field `QLineEdit` biasa, termasuk Pengaturan Toko.
- Menonaktifkan clear button pada seluruh `QLineEdit` dan input internal numeric spinbox.
- Menambahkan regression test global.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.13**.

### 2.3.12
- Menghapus ikon dekoratif dari shell modern, termasuk ikon menu sidebar dan simbol dekoratif Dashboard.
- Mempertahankan logo WPOS sebagai identitas aplikasi.
- Menambahkan regression coverage untuk UI text-first.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.12**.

### 2.3.11
- Menghapus ikon dekoratif dari seluruh menu sidebar modern.
- Sidebar hanya menampilkan nama section dan teks menu.
- Mempertahankan `Qt.UserRole` dan index navigasi.
- Menambahkan dokumentasi sidebar text-only.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.11**.

### 2.3.10
- Memperbaiki clear button pada `QDoubleSpinBox`/`QSpinBox`.
- Menambahkan marker `wposClearButtonDisabled` dan regression test numeric spinbox.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.10**.

### 2.3.9
- Menghapus aktivasi global tombol clear **×** pada seluruh `QLineEdit`.
- Mempertahankan normalisasi geometry field input.
- Menambahkan regression test global.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.9**.

### 2.3.8
- Memperbaiki geometry halaman **Kasir** berdasarkan audit screenshot produksi.
- Memperlebar panel Ringkasan Pembayaran.
- Memberi ukuran minimum pada tombol CLEAR dan BAYAR & CETAK.
- Menambahkan regression test geometry pembayaran.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.8**.

### 2.3.7
- Memperbaiki tampilan Dashboard.
- Menghilangkan header/branding Dashboard internal yang menyisakan area kosong.
- Memusatkan sambutan pada topbar modern.
- Mempertahankan KPI harian dan saldo kas berjalan.
- Menambahkan regression coverage.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.7**.

### 2.3.6
- Memperbaiki Dashboard agar TRANSAKSI dan OMZET menggunakan rentang hari kalender lokal.
- Memisahkan SALDO KAS sebagai saldo berjalan.
- Welcome header memakai username dan tanggal komputer aktual.
- Memperbarui regression test.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.6**.

### 2.3.5
- Memperbaiki deteksi `QGroupBox` pada hybrid form Produk dan Pembelian.
- Menjaga popup/inline sebagai perubahan presentasi UI.
- Menambahkan regression coverage 14 halaman.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.5**.

### 2.3.4
- Menerapkan hybrid form UX pada 14 halaman.
- Produk, Pembelian, Supplier dan Pelanggan menggunakan popup.
- Kategori dan Satuan menggunakan form inline/horizontal.
- Stok & Mutasi, Kas, Pengaturan Toko dan Printer mempertahankan pola input cepat/horizontal.
- Menambahkan `app/ui/form_layouts.py` sebagai presentation layer.
- Menambahkan regression test.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.4**.

### 2.3.3
- Mengganti branding strip Dashboard dengan welcome header sesuai desain.
- Menjaga kompatibilitas Dark/Light Mode.
- Menambahkan regression test Dashboard Welcome Header.

### 2.3.2
- Memperbaiki Light Mode agar sidebar modern mengikuti palette Light Mode.
- Menambahkan `sidebar_text` dan `sidebar_inverse` serta regression test.

### 2.3.0–2.3.1
- 2.3.0: Dark Mode dijadikan tema tunggal setelah Modern Blue, Purple Premium dan Emerald dihapus.
- 2.3.1: Light Mode ditambahkan kembali sebagai tema resmi bersama Dark Mode.
- Key tema lama/tidak valid fallback ke DARK.

### Riwayat sebelumnya
Riwayat versi sebelum 2.3.0 tetap dapat ditelusuri melalui Git history repository.
