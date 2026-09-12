# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.7.16**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Perubahan terbaru 2.7.16
- Memperkuat validasi Backup / Restore database SQLite sebelum database aktif diganti.
- Menambahkan pemeriksaan `PRAGMA integrity_check` dan validasi tabel inti pada file backup.
- Membuat safety backup database aktif sebelum proses restore.
- Menambahkan regression test untuk backup invalid, integrity check, safety backup dan restore valid.
- Menetapkan **2.7.16** sebagai patch release stabilisasi.
- Setiap perubahan versi wajib dicatat di README dan Changelog.

## Perubahan terbaru 2.7.15
- Menstabilkan CI dengan menjadikan workflow Windows Build dan Windows Installer sebagai **manual dispatch** sementara runner Windows GitHub mengalami kegagalan sebelum step pertama.
- Menambahkan workflow independen `ci-health.yml` pada Ubuntu untuk memvalidasi checkout, Python, dependency, compile dan pytest tanpa bergantung pada Windows runner.
- Menyinkronkan config, installer dan regression test ke versi **2.7.15**.
- Tidak mengubah UI, authentication flow, database, schema, atau business logic.

## Build Windows aktif
- `windows-build.yml`: build EXE Windows otomatis pada push ke `main` dan tetap tersedia melalui `workflow_dispatch`.
- `windows-installer.yml`: build installer Windows otomatis pada push ke `main` dan tetap tersedia melalui `workflow_dispatch`.
- Kedua workflow menggunakan `windows-2022`, Python 3.12, compileall, pytest, PyInstaller, pemeriksaan branding, dan validasi output.
- Artifact build: `WPOS-PRO-2-Windows`.
- Artifact installer: `WPOS-PRO-2-Installer`.

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

## Versioning
Menggunakan **Semantic Versioning (MAJOR.MINOR.PATCH)**.
- **PATCH**: bug fix, hardening, stabilisasi, test, dokumentasi atau perubahan internal tanpa breaking change.
- **MINOR**: fitur baru yang backward-compatible.
- **MAJOR**: breaking change atau perubahan kontrak yang memerlukan migrasi/penyesuaian pengguna.
- Nomor versi adalah milestone release, bukan nomor setiap commit.
- Setiap perubahan versi wajib memperbarui **README.md**, **CHANGELOG.md**, `app/config.py`, metadata installer/build yang relevan, dan regression test versi bila diperlukan.
- Release final harus konsisten antara source, EXE, installer, Git tag dan release notes.
- Urutan release gate: **Audit → Fix → Test → Version Gate → Build → EXE Validation → Installer → Checksum → Release Candidate**.

## Changelog
### 2.7.16
- Hardening Backup / Restore SQLite.
- Backup restore sekarang menolak file yang corrupt atau tidak memiliki tabel inti yang diperlukan.
- Database aktif dibuatkan safety backup sebelum restore mengganti database.
- Menambahkan regression test untuk validasi backup, integrity check, safety backup dan restore valid.
- Patch release untuk stabilisasi dan keamanan data.

### 2.7.15
- Menjadikan Windows Build dan Windows Installer sebagai manual dispatch sementara.
- Menambahkan `ci-health.yml` untuk health check otomatis di Ubuntu.
- Menyinkronkan config, installer dan regression test ke **2.7.15**.
- Tidak mengubah schema/database/business logic.

### 2.7.14
- Mengubah runner Windows dari `windows-latest` menjadi `windows-2022` pada Build dan Installer.
- Menambahkan diagnostic runner untuk memperjelas image/runner bila job gagal sebelum build.
- Menyinkronkan `app/config.py`, `installer.iss`, dan regression test ke **2.7.14**.
- Tidak mengubah schema/database/business logic.

### 2.7.13
- Memperbaiki test `test_version_and_docs_are_synchronized` yang masih mengharapkan versi **2.7.10**.
- Menyinkronkan test dengan versi aplikasi baru.
- Menyinkronkan `app/config.py` dan `installer.iss` ke **2.7.13**.
- Perubahan ini dibuat untuk memperbaiki kegagalan CI run #294.
- Tidak mengubah schema/database/business logic.

## Struktur sidebar
- **OPERASIONAL:** Dashboard, Kasir, Produk, Stok & Mutasi, Pembelian.
- **KEUANGAN:** Kas, Laporan.
- **DATA MASTER:** Pelanggan, Supplier, Kategori, Satuan.
- **SYSTEM:** Pengaturan Toko, Printer, Backup / Restore.
- Text-only tanpa ikon dekoratif.
- Lebar sidebar 230 px.
- Active menu dan hover mengikuti tema.

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

## CI
- `ci-health.yml`: health check otomatis di Ubuntu untuk compile dan pytest.
- `windows-build.yml`: build EXE Windows otomatis pada push ke `main` atau melalui **workflow_dispatch**.
- `windows-installer.yml`: build installer Windows otomatis pada push ke `main` atau melalui **workflow_dispatch**.
- Workflow Windows menggunakan `windows-2022` dan diagnostic runner.
- Artifact hasil build tersedia pada masing-masing workflow jika seluruh validasi berhasil.

## Tema
- **Dark Mode** — default.
- **Light Mode**.
- Tema lama dihapus dan key invalid fallback ke DARK.

## Numeric Input
- Input desktop angka bulat menggunakan langkah 1.
- `1` tetap `1`, `2` tetap `2`, `10` tetap `10`.
- Tampilan stok bulat dinormalisasi tanpa mengubah database.
- Nilai pecahan yang benar tetap dipertahankan.
- Tidak ada faktor ×1.000.

## UI
- Sidebar text-only 230 px.
- Headerbar tiga zona: Context kiri, Nama Toko tengah, Pengguna + Tanggal kanan.
- Kasir menggunakan struktur Input Produk → Keranjang + Pembayaran → Kontrol Transaksi.
- Form Produk, Pembelian, Supplier dan Pelanggan menggunakan popup hybrid.
- Kategori dan Satuan menggunakan form inline/horizontal.
- Footer: **Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana**.
- Login tidak mengulang versi aplikasi karena versi sudah tersedia di Footer.

## Excel Produk
- Export `.xlsx`.
- Template `.xlsx`.
- Import Tambah atau Update berdasarkan Barcode.
- Update tidak mengubah stok berjalan.

## Arsitektur
- `app/ui/modern_main_window.py` — shell/sidebar/topbar/stack.
- `app/ui/main_window.py` — halaman dan workflow bisnis.
- `app/ui/premium_cashier.py` — UI Kasir.
- `app/ui/cashier_structure.py` — struktur presentasi Kasir.
- `app/ui/headerbar.py` — struktur Headerbar.
- `app/ui/product_display.py` — presentasi Stok dan Status tabel Produk.
- `app/ui/master_data.py` — CRUD master data.
- `app/ui/form_layouts.py` — hybrid form, Excel, reset dan kontrol Produk.
- `app/ui/global_ui.py` — aturan global UI.
- `app/ui/theme_shell.py` — palette dan styling.
- `app/services/product_delete.py` — penghapusan Produk aman.
- `app/services/receipt_display.py` — presentasi Qty struk.
