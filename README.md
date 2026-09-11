# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.3.4**
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
Pada **v2.3.3**, branding strip lama pada Dashboard diganti menjadi header sambutan:
- **Selamat datang, Admin**
- **Senin, 12 September 2026**

Header menggunakan surface dan teks yang mengikuti tema aktif sehingga tidak lagi tampil sebagai strip branding biru pada Dashboard.

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
**WPOS PRO 2 — v2.3.4.** Hybrid form UX selesai; menunggu CI PASS dan verifikasi Windows/thermal printer/installer sebelum release final.
