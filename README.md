# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.1.1**
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

## Tema aplikasi
WPOS PRO 2 menyediakan empat tema aktif:
- **Modern Blue** — tampilan biru modern dan netral.
- **Purple Premium** — tampilan ungu premium dan elegan.
- **Emerald** — tampilan hijau emerald yang profesional dan bersih.
- **Dark Mode** — tampilan gelap untuk penggunaan dengan kontras rendah.

Tema **Kemerdekaan** dan **Keagamaan** telah dihapus dari daftar aktif.
Jika database lokal sebelumnya menyimpan salah satu tema lama, aplikasi otomatis kembali ke **Modern Blue** agar tidak terjadi tema yang tidak tersedia.

## Footer aplikasi
Footer modern shell dan login menggunakan **komponen footer bersama** dengan struktur yang sama:
**Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana**

Spesifikasi footer:
- Tinggi tetap **30 px**.
- Teks kecil **10 px** dan tidak dominan.
- Login dan modern shell menggunakan helper footer yang sama: `add_application_footer()`.
- Keduanya menggunakan object/style `applicationFooter` dan `applicationFooterLabel` yang sama.
- Footer login berada di bagian bawah dialog login dan tetap ringkas.
- Footer modern shell berada setelah area `QStackedWidget`, sehingga tetap menempel di bagian bawah modern content pada seluruh halaman.
- Footer tidak menjadi bagian dari halaman individual dan tidak ikut bergeser saat navigasi.
- Nama dan versi mengikuti `APP_NAME` / `APP_VERSION`; tahun mengikuti tahun sistem saat aplikasi dijalankan.

## Dashboard UI
- Branding dashboard mengikuti `APP_NAME`, sehingga tidak lagi menampilkan identitas lama **WPOS PRO**.
- Judul window mengikuti nama aplikasi **WPOS PRO 2**.
- Tabel Dashboard yang belum memiliki data menampilkan empty-state yang ringkas dan informatif.
- Tooltip instruksi keyboard pada tabel dihapus agar tidak muncul sebagai overlay saat pointer berada di area tabel.
- Perubahan hanya menyentuh presentasi/UX; tidak membuat transaksi, produk, atau data stok baru.

## Versioning
Aturan versi resmi WPOS PRO 2:
- **Perubahan besar / fitur besar:** naik **MINOR**. Contoh `2.0.1` → `2.1.0`.
- **Perbaikan / perubahan kecil:** naik **PATCH**. Contoh `2.0.1` → `2.0.2`.
- **Setiap perubahan source, konfigurasi, build, CI, atau dokumentasi** wajib dicatat di README dan menggunakan kenaikan versi yang sesuai dengan jenis perubahannya.
- Versi aktif saat ini: **2.1.1**.

## Changelog
### 2.1.1
- Memperbaiki branding Dashboard agar seluruh identitas mengikuti **WPOS PRO 2**.
- Menyamakan judul window dengan `APP_NAME` sehingga tidak lagi menggunakan teks **WPOS PRO V2**.
- Menambahkan empty-state Dashboard untuk kondisi belum ada transaksi dan belum ada stok yang perlu diperhatikan.
- Menghapus tooltip instruksi tabel yang dapat muncul sebagai overlay di area Dashboard.
- Menyinkronkan `APP_VERSION` dan metadata installer ke **2.1.1**.
- Tidak mengubah business logic atau database schema.

### 2.1.0
- Menghapus tema **Kemerdekaan** dari daftar tema aktif.
- Menghapus tema **Keagamaan** dari daftar tema aktif.
- Menambahkan tema **Purple Premium**.
- Menambahkan tema **Emerald**.
- Menjaga **Modern Blue** dan **Dark Mode**.
- Menambahkan fallback otomatis ke Modern Blue jika database lokal masih menyimpan key tema lama yang sudah dihapus.
- Menambahkan style footer yang konsisten pada seluruh tema baru.
- Menyinkronkan versi aplikasi dan metadata installer ke **2.1.0**.
- Tidak mengubah business logic atau database schema.

### 2.0.7
- Menjadikan footer Login dan modern shell menggunakan helper `add_application_footer()` yang sama.
- Menyatukan implementasi geometry: tinggi **30 px**, size policy fixed secara vertikal, margin horizontal **8 px**, spacing **0**, teks terpusat, dan object/style yang sama.
- Menghapus implementasi footer Login yang terpisah agar tidak terjadi perbedaan visual/geometry pada masa depan.
- Menyinkronkan versi aplikasi dan metadata installer ke **2.0.7**.
- Tidak mengubah business logic atau database.

### 2.0.6
- Menyamakan footer halaman Login dengan footer modern shell.
- Menggunakan struktur **Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana** pada Login.
- Menggunakan object/style footer yang sama: `applicationFooter` dan `applicationFooterLabel`.
- Menetapkan tinggi footer Login **30 px**, teks **10 px**, dan alignment terpusat.
- Menghapus format footer Login lama yang berbeda (`©` dan `Created by`).
- Tidak mengubah business logic atau database.

### 2.0.5
- Menetapkan tinggi footer secara eksplisit **30 px**.
- Menetapkan size policy footer agar horizontal mengikuti area content tetapi vertikal tetap fixed.
- Menetapkan style global `applicationFooter` dengan rentang efektif 30 px.
- Memastikan teks footer tetap kecil, terpusat, dan tidak dominan.
- Footer tetap berada di bawah `modernStack`, sehingga konsisten untuk seluruh halaman tanpa mengambil ruang besar.
- Tidak mengubah business logic atau database.

### 2.0.4
- Menyederhanakan footer aplikasi menjadi struktur: **Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana**.
- Tahun footer diambil otomatis dari tahun sistem saat aplikasi dijalankan.
- Footer menggunakan `APP_NAME` dan `APP_VERSION`, sehingga identitas selalu mengikuti versi aplikasi.
- Menjaga footer tetap berada di area bawah modern content dan tidak mengubah business logic atau database.
- Menyinkronkan metadata installer ke versi **2.0.4**.

### 2.0.3
- Memperbaiki geometri `QSpinBox` dan `QDoubleSpinBox` agar field tidak terlalu sempit.
- Menetapkan lebar minimum field numeric dan ruang kanan yang cukup untuk kontrol naik/turun.
- Menormalkan ukuran tombol increment/decrement agar tidak terlihat menumpuk atau terpotong.
- Menjaga tinggi kontrol numeric tetap konsisten dengan field input lainnya.
- Menyinkronkan versi installer Inno Setup dari 2.0.0 menjadi **2.0.3**.
- Perubahan ini hanya menyentuh layout/UX dan metadata build; tidak mengubah business logic atau database.

### 2.0.2
- Perbaikan layout global agar lebih konsisten dan responsif.
- Membatasi ukuran form/card agar tidak melebar berlebihan pada layar besar.
- Menormalkan spacing halaman dalam rentang yang lebih stabil.
- Menyempurnakan tabel: resize kolom lebih terkendali, kolom terakhir tetap mengisi ruang, dan ukuran minimum kolom dijaga.
- Menyempurnakan perilaku horizontal/vertical scrollbar pada `QScrollArea`.
- Perubahan ini hanya menyentuh presentasi/geometri UI dan tidak mengubah business logic atau database.

### 2.0.1
- Menaikkan versi aplikasi dari **2.0.0** menjadi **2.0.1**.
- Menetapkan aturan versioning: perubahan besar menaikkan MINOR, sedangkan perbaikan/perubahan kecil menaikkan PATCH.
- README disinkronkan dengan aturan versioning resmi.

### 2.0.0
- Standardisasi identitas aplikasi menjadi **WPOS PRO 2**.
- Sinkronisasi nama aplikasi, data directory, EXE, dist, installer, dan asset branding.
- Perbaikan build Windows dan installer agar menggunakan branding yang konsisten.
- Perbaikan branding modern shell agar mengikuti `APP_NAME`.
- Penghapusan duplicate import di `app/main.py`.
- Penambahan regression test untuk branding/build asset dan navigasi.

## Status
**WPOS PRO 2 — v2.1.1.** Kandidat release setelah CI PASS dan verifikasi Windows/thermal printer/installer.