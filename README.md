# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.5.0**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

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

## CRUD dan kontrol data
- **Produk:** Tambah, Edit, Simpan, Nonaktifkan. Penghapusan permanen tidak digunakan agar histori transaksi tetap aman.
- **Kategori:** Tambah, Edit, Simpan, Hapus.
- **Satuan:** Tambah, Edit, Simpan, Hapus.
- **Supplier:** Tambah, Edit, Simpan, Hapus.
- **Pelanggan:** Tambah, Edit, Simpan, Hapus.
- Master data dapat dipilih dengan klik baris tabel; data terpilih dimuat kembali ke form untuk diedit.
- Hapus master yang masih direferensikan oleh produk atau pembelian ditolak untuk melindungi integritas histori.
- **Stok & Mutasi:** tambah/simpan mutasi; koreksi dilakukan sebagai mutasi baru, bukan menghapus histori.
- **Pembelian:** tambah/simpan transaksi; pembatalan transaksi yang mempengaruhi stok harus menggunakan reversal, bukan delete langsung.
- **Kas:** tambah/simpan transaksi; koreksi dilakukan dengan reversal agar histori kas tidak hilang.
- **Dashboard/Laporan:** read-only.
- **Pengaturan Toko/Printer:** edit dan simpan konfigurasi.
- **Backup/Restore:** action-based.

## Reset Data
Tersedia di halaman **Backup / Restore** untuk ADMIN:
- **RESET TRANSAKSI & STOK** — menghapus penjualan, item penjualan, pembelian, item pembelian, mutasi stok dan mutasi kas; seluruh stok produk dikembalikan ke `0`. Master produk/kategori/satuan/supplier/pelanggan tetap ada.
- **RESET SEMUA DATA BISNIS** — menghapus seluruh transaksi, mutasi dan semua master bisnis (produk, kategori, satuan, supplier, pelanggan).
- Akun pengguna dan pengaturan toko **tidak ikut dihapus**.
- Reset memakai konfirmasi dua tahap dan pengguna wajib mengetik **RESET**.
- Reset dilakukan dalam urutan yang aman terhadap foreign key.
- Setelah reset, aplikasi diminta ditutup dan dijalankan kembali agar seluruh halaman memuat data terbaru.
- Backup tetap disarankan sebelum reset karena reset bersifat permanen.

## Alur kasir
Barcode → Keranjang → Diskon → Pembayaran → Kembalian → Stok berkurang → Transaksi tersimpan → Cetak struk.

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
- Mutation service melakukan rollback pada kegagalan commit.

## Keamanan
- Password PBKDF2-SHA256 dengan salt acak.
- User inactive tidak dapat login.
- Minimal satu Administrator aktif.
- Mutation user memiliki rollback protection.

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
- Modern Blue, Purple Premium, Emerald, Kemerdekaan dan Keagamaan sudah dihapus.
- Key tema invalid/lama fallback ke DARK.

## Numeric Input
- Input desktop angka bulat menggunakan langkah 1.
- `1` tetap `1`, `2` tetap `2`, `10` tetap `10`.
- Tampilan stok bulat seperti `24.000` dinormalisasi menjadi `24` tanpa mengubah database.
- Nilai pecahan yang benar tetap dipertahankan.
- Tidak ada faktor ×1.000.
- Data database lama tidak dimigrasikan atau dikalikan otomatis.

## UI
- Sidebar navigasi text-only tanpa ikon menu.
- Form Produk, Pembelian, Supplier dan Pelanggan menggunakan popup hybrid.
- Kategori dan Satuan menggunakan form inline/horizontal.
- Clear button `×` dikendalikan oleh global UI dan tidak diaktifkan kembali oleh layer UX.
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
### 2.5.0
- Menambahkan fitur **Reset Data** pada halaman Backup / Restore.
- Menambahkan **RESET TRANSAKSI & STOK** untuk membersihkan histori transaksi/mutasi dan mengosongkan stok tanpa menghapus master data.
- Menambahkan **RESET SEMUA DATA BISNIS** untuk membersihkan seluruh data bisnis tanpa menghapus akun pengguna dan pengaturan toko.
- Reset dilindungi konfirmasi dua tahap dan wajib mengetik `RESET`.
- Penghapusan dilakukan dalam urutan FK-safe.
- Menambahkan regression tests untuk kedua mode reset.
- Menyinkronkan `APP_VERSION` dan installer ke **2.5.0**.
- Tidak mengubah schema database.

### 2.4.4
- Melengkapi CRUD master data **Kategori, Satuan, Supplier dan Pelanggan**.
- Menambahkan pemilihan baris tabel untuk memuat data kembali ke form.
- Menambahkan mode Edit dan Simpan Perubahan.
- Menambahkan Hapus Terpilih dengan konfirmasi.
- Penghapusan master yang masih digunakan produk/pembelian diblokir untuk menjaga integritas data.
- Produk tetap menggunakan Nonaktifkan, bukan delete permanen.
- Menambahkan regression test untuk create/edit/delete dan dependency protection.
- Menyinkronkan versi aplikasi dan installer ke **2.4.4**.

### 2.4.3
- Menormalkan tampilan stok bulat agar `24.000` tampil sebagai `24` tanpa mengubah nilai database.
- Nilai pecahan tetap dipertahankan.

### 2.4.2
- Numeric input desktop menggunakan presisi 0 dan langkah 1 untuk menghilangkan ambiguitas `1.000`.
- Tidak ada pengali ×1.000.

### 2.4.1
- Perbaikan tampilan numeric input dan regression test.

### 2.4.0
- Export, Template dan Import Produk Excel.
- Import mendukung Tambah dan Update Barcode.
- Update tidak mengubah stok berjalan.
- Menambahkan dependency openpyxl dan regression tests.

### 2.3.16
- Role resmi menjadi ADMIN dan KASIR.
- PENGELOLA dan TEKNISI dihapus dari permission policy.

### 2.3.15
- Hardening validasi Decimal dan rollback mutation user/settings.

### 2.3.14
- Menetapkan `global_ui.py` sebagai sumber tunggal clear-button policy dan menghapus override UX.

### 2.3.13
- Clear button dinonaktifkan secara global pada input.

### 2.3.12 / 2.3.11
- Sidebar modern menjadi text-first tanpa ikon dekoratif.

### 2.3.3
- Dashboard welcome header menggunakan nama user dan tanggal lokal.

### 2.3.2
- Light Mode sidebar mengikuti palette Light Mode.

### 2.3.1
- Menambahkan Light Mode; Dark Mode tetap default.

### 2.3.0
- Modern Blue, Purple Premium dan Emerald dihapus; Dark Mode menjadi tema utama sebelum Light Mode ditambahkan.

## Arsitektur
- `app/ui/modern_main_window.py` — shell/sidebar/topbar/stack.
- `app/ui/main_window.py` — halaman dan workflow.
- `app/ui/master_data.py` — CRUD master data.
- `app/ui/form_layouts.py` — hybrid form, Excel UI dan Reset Data.
- `app/ui/global_ui.py` — aturan global kontrol/geometry.
- `app/ui/theme_shell.py` — palette DARK/LIGHT.
- `app/ui/ux2026.py` — interaction/accessibility.
- `app/services/reset.py` — reset data bisnis dengan FK-safe deletion.
- `app/services/` — business logic.
- `app/models.py` — database model.
