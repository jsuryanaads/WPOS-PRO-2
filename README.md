# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.3.2**
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

Asset branding:
- `assets\\branding\\wpos_logo.png`
- `assets\\branding\\wpos_icon.ico`

Hasil build:
`dist\\WPOS PRO 2\\WPOS PRO 2.exe`

## Installer
Compile `installer.iss` menggunakan Inno Setup.

Hasil installer:
`installer\\WPOS_PRO_2_Setup.exe`

## CI
GitHub Actions menjalankan compile check dan test suite pada push/PR. Windows build memverifikasi source, test, EXE, associated icon, serta asset branding.

## Tema aplikasi
Mulai **v2.3.2**, aplikasi menyediakan dua tema resmi:
- **Dark Mode** — tema default.
- **Light Mode** — tema terang dengan surface putih, kontras teks gelap dan aksen biru; sidebar juga mengikuti palette Light Mode.

Tema yang sudah dihapus dan tidak tersedia:
- Modern Blue
- Purple Premium
- Emerald

Key tema lama atau tidak valid yang tersimpan di database otomatis fallback ke **DARK**. Menu **Tema** sekarang menampilkan **Dark Mode** dan **Light Mode**.

## Footer aplikasi
Struktur bersama:
**Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana**

Spesifikasi:
- Tinggi tetap **30 px**.
- Teks **10 px**.
- Login dan modern shell memakai helper `add_application_footer()`.
- Object/style: `applicationFooter` dan `applicationFooterLabel`.
- Footer modern berada di luar `QStackedWidget` sehingga konsisten pada seluruh halaman.

## Audit & perbaikan 14 halaman — v2.2.0
Audit difokuskan pada presentasi, geometri, konsistensi dan usability tanpa mengubah business logic atau database schema.

Perbaikan global yang diterapkan ke seluruh 14 halaman:
- Spacing halaman dinormalisasi ke rentang **8–12 px**.
- Margin halaman dinormalisasi menjadi **16 / 8 / 16 / 12 px**.
- Form menggunakan `DontWrapRows`, label alignment konsisten, horizontal spacing 12 px dan vertical spacing 5 px.
- GroupBox dibatasi agar form tidak melebar berlebihan.
- Tabel memakai row selection, single selection, non-editable, alternating rows, row height 34 px dan kolom terakhir mengisi ruang.
- Horizontal/vertical scrollbar tabel dibuat `AsNeeded`.
- Field input minimum 32 px dan numeric field minimum 110 px.
- Tombol dinormalisasi agar tidak mengambil ukuran berlebihan dan memakai cursor pointer.
- QScrollArea dibuat resizable dan scrollbar hanya muncul saat diperlukan.
- Header halaman lama disembunyikan ketika modern shell sudah menyediakan judul/subjudul, sehingga tidak ada duplikasi header.
- Dashboard card diberi batas lebar agar lima metric tidak melebar berlebihan.
- Settings, Printer dan Backup/Restore dibatasi lebar form agar lebih terkontrol pada monitor besar.
- Master pages (Kategori, Satuan, Supplier, Pelanggan) memakai kontrak tabel/form yang sama.
- Window identity dipaksa mengikuti `APP_NAME` sehingga tidak kembali ke **WPOS PRO V2**.
- Tidak mengubah transaksi, stok, laporan, kas, database, atau aturan bisnis.

### Status audit 14 halaman
| Halaman | Status |
|---|---|
| Dashboard | ✅ Layout, metric cards, tabel, spacing |
| Kasir | ✅ Area input, tabel keranjang, pembayaran |
| Produk | ✅ Form, numeric fields, tabel |
| Stok & Mutasi | ✅ Form, tabel, scrollbar |
| Pembelian | ✅ Form, tabel, spacing |
| Kas | ✅ Form dan tabel transaksi |
| Laporan | ✅ Tabel dan ruang kerja |
| Pengaturan Toko | ✅ Form tidak melebar |
| Printer | ✅ Form tidak melebar |
| Backup / Restore | ✅ Form dan scrollbar |
| Kategori | ✅ Master form + tabel |
| Satuan | ✅ Master form + tabel |
| Supplier | ✅ Master form + tabel |
| Pelanggan | ✅ Master form + tabel |

## Versioning
Aturan versi resmi:
- **Perubahan besar / fitur besar:** naik **MINOR**, contoh `2.2.0` → `2.3.0`.
- **Perbaikan / perubahan kecil:** naik **PATCH**, contoh `2.2.0` → `2.2.1`.
- Setiap perubahan source, konfigurasi, build, CI atau dokumentasi wajib dicatat di README dan menggunakan kenaikan versi yang sesuai.

## Changelog
### 2.3.2
- Memperbaiki **Light Mode** agar sidebar modern tidak lagi mempertahankan warna gelap.
- Sidebar, navigasi, brand/account panel, hover dan logout mengikuti palette Light Mode.
- Menambahkan warna khusus `sidebar_text` dan `sidebar_inverse` agar kontras teks sidebar tetap terbaca.
- Menambahkan regression test untuk memastikan stylesheet sidebar memakai palette Light Mode.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.2**.
- Tidak mengubah business logic atau database schema.

### 2.3.1
- Menambahkan **Light Mode** sebagai tema resmi baru.
- Mempertahankan **Dark Mode** sebagai tema default.
- Menghapus Modern Blue, Purple Premium dan Emerald tetap berlaku.
- Menambahkan palette Light Mode pada registry tema dan shell modern.
- Menambahkan fallback tema tidak valid ke DARK tanpa mengubah schema database.
- Memperbarui regression test untuk memastikan registry tema berisi DARK dan LIGHT.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.1**.
- Tidak mengubah business logic atau database schema.

### 2.3.0
- Menetapkan **Dark Mode** sebagai satu-satunya tema resmi WPOS PRO 2.
- Menghapus **Modern Blue**, **Purple Premium**, dan **Emerald** dari registry tema.
- Menghapus palette shell Modern Blue, Purple Premium, dan Emerald dari `theme_shell.py`.
- Mengubah fallback tema database dari Modern Blue menjadi **DARK**.
- Key tema lama yang tersimpan otomatis dinormalisasi ke DARK.
- Menu Tema hanya menampilkan Dark Mode.
- Menambahkan regression test yang memastikan registry tema hanya berisi DARK.
- Menyinkronkan `APP_VERSION` dan installer ke **2.3.0**.
- Tidak mengubah business logic atau database schema.

### 2.2.0
- Audit dan normalisasi layout **seluruh 14 halaman**.
- Menetapkan kontrak geometry/UX global agar form, tabel, tombol dan scrollbar konsisten.
- Mengurangi form yang terlalu lebar pada monitor besar.
- Menstabilkan tinggi tabel dan field numeric.
- Menormalkan perilaku tabel dan scrollbar.
- Menghilangkan duplikasi header halaman pada modern shell.
- Menyamakan geometry master pages Kategori, Satuan, Supplier dan Pelanggan.
- Menyelaraskan shell theme dengan empat tema aktif: Modern Blue, Purple Premium, Emerald dan Dark Mode.
- Menghapus sisa palette Kemerdekaan dan Keagamaan dari `theme_shell.py`.
- Menyamakan identitas window dengan `APP_NAME`.
- Menyinkronkan `APP_VERSION` dan installer ke **2.2.0**.
- Tidak mengubah business logic atau database schema.

### 2.1.1
- Memperbaiki branding Dashboard agar seluruh identitas mengikuti **WPOS PRO 2**.
- Menyamakan judul window dengan `APP_NAME`.
- Menambahkan empty-state Dashboard.
- Menghapus tooltip instruksi tabel yang mengganggu.
- Menyinkronkan versi aplikasi dan installer ke **2.1.1**.

### 2.1.0
- Menghapus tema Kemerdekaan dan Keagamaan dari daftar aktif.
- Menambahkan Purple Premium dan Emerald.
- Menjaga Modern Blue dan Dark Mode.
- Menambahkan fallback Modern Blue untuk key tema lama.
- Menyinkronkan installer ke 2.1.0.

### 2.0.7
- Menyatukan footer Login dan modern shell menggunakan `add_application_footer()`.
- Footer fixed 30 px dengan object/style yang sama.

### 2.0.6
- Menyamakan footer Login dengan modern shell.

### 2.0.5
- Menetapkan geometry footer 30 px dan positioning bawah modern content.

### 2.0.4
- Menyederhanakan footer menjadi struktur Nama aplikasi | Versi | Tahun | by Jsuryana.

### 2.0.3
- Memperbaiki geometri QSpinBox/QDoubleSpinBox dan tombol numeric.

### 2.0.2
- Perbaikan layout global, form/card, tabel dan scrollbar.

### 2.0.1
- Menetapkan aturan versioning MINOR/PATCH.

### 2.0.0
- Standardisasi identitas aplikasi menjadi WPOS PRO 2.
- Sinkronisasi nama aplikasi, data directory, EXE, installer dan branding.

## Status
**WPOS PRO 2 — v2.3.2.** Perubahan sidebar Light Mode selesai; menunggu CI PASS dan verifikasi Windows/thermal printer/installer sebelum release final.
