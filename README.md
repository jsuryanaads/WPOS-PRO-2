# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.8.2**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Perubahan terbaru 2.8.2
- Memperbaiki Headerbar agar update dilakukan pada widget yang sudah ada tanpa `setParent(None)` atau `layout.removeItem`.
- Menjaga ownership/lifetime widget Qt tetap stabil saat UI direfresh atau berpindah halaman.
- Headerbar menampilkan **judul + hint halaman aktif** di kiri, **nama toko + alamat toko** di tengah, dan **nama display user + tanggal Indonesia** di kanan.
- `Dashboard Welcome` tidak lagi menimpa Headerbar global dengan username atau tanggal legacy.
- Menambahkan regression test untuk kontrak Headerbar ownership-safe dan pemisahan Dashboard.
- Tidak mengubah business logic transaksi, database, authentication, atau struktur 14 halaman.
- Release **2.8.2** dikategorikan sebagai PATCH karena merupakan bug fix/hardening backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

## Perubahan terbaru 2.8.0
- Menambahkan **Nama lengkap user** pada Manajemen User.
- Menambahkan **Simpan Perubahan** untuk nama, role dan status user.
- Menambahkan **Hapus User** dengan konfirmasi dan perlindungan akun penting.
- Username dikunci saat edit untuk menjaga identitas login.
- Role resmi aplikasi distandarkan menjadi `ADMIN` dan `KASIR`; role legacy `TEKNISI` dinormalisasi menjadi `KASIR`.
- Menambahkan perlindungan agar Administrator aktif terakhir tidak dapat dihapus atau dinonaktifkan.
- Menambahkan perlindungan agar user tidak dapat menghapus akun yang sedang digunakan.
- Tabel Manajemen User sekarang menampilkan ID, Nama, Username, Role dan Status.
- Release **2.8.0** dikategorikan sebagai MINOR karena menambahkan functionality backward-compatible dan field Nama pada schema user.

## Perubahan terbaru 2.7.17
- Menerapkan aturan UI global pada seluruh 14 halaman: background dekoratif di belakang label dibuat transparan secara default.
- Menghilangkan pola visual **box inside box** yang tidak memiliki fungsi UI.
- Background fungsional tetap dipertahankan pada input, tombol, tabel, card, badge/status dan panel.
- Label sekarang mengikuti surface parent secara konsisten sehingga UI lebih bersih dan ringan.
- Tidak mengubah business logic, database schema, authentication flow atau perilaku transaksi.

## Perubahan terbaru 2.7.16
- Memperkuat validasi Backup / Restore database SQLite sebelum database aktif diganti.
- Menambahkan pemeriksaan `PRAGMA integrity_check` dan validasi tabel inti pada file backup.
- Membuat safety backup database aktif sebelum proses restore.
- Menambahkan regression test untuk backup invalid, integrity check, safety backup dan restore valid.
- Menetapkan **2.7.16** sebagai patch release stabilisasi.

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

## Struktur sidebar
- **OPERASIONAL:** Dashboard, Kasir, Produk, Stok & Mutasi, Pembelian.
- **KEUANGAN:** Kas, Laporan.
- **DATA MASTER:** Pelanggan, Supplier, Kategori, Satuan.
- **SYSTEM:** Pengaturan Toko, Printer, Backup / Restore.
- Text-only tanpa ikon dekoratif.
- Lebar sidebar 230 px.
- Active menu dan hover mengikuti tema.

## Struktur Headerbar FINAL
```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ KASIR                    TOKO SEMBAKO SAPNI                 Jajang Suryana  │
│ Transaksi cepat · barcode first                              12 September  │
│                              Alamat Toko                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```
- **Kiri:** judul halaman aktif + subtitle/hint dinamis; berubah mengikuti halaman yang dipilih.
- **Tengah:** nama toko + alamat toko dari `Pengaturan Toko`, selalu diposisikan center.
- **Kanan:** **Nama** pengguna yang sedang login + tanggal otomatis dalam format Indonesia.
- Username login tidak ditampilkan di Headerbar.
- Status OFFLINE/DATABASE LOKAL tidak ditampilkan di Headerbar.

## Aturan UI Global
- **One purpose, one container.**
- Label tidak menggunakan background dekoratif sendiri.
- `QLabel` menggunakan background transparan secara default.
- Teks ditempatkan langsung di atas surface parent jika tidak membutuhkan container khusus.
- Background tetap boleh digunakan untuk komponen yang memang memiliki fungsi visual/interaktif: input, tombol, tabel, card, badge/status dan panel.
- Hindari **box inside box** yang tidak diperlukan.
- Spacing, typography, border dan hierarchy digunakan untuk membedakan informasi.
- Seluruh 14 halaman mengikuti kontrak visual yang sama.

## Struktur Manajemen User PRO
- Form user: Nama, Username, Password, Role, Status.
- Role resmi: `ADMIN` dan `KASIR`.
- Tambah User, Simpan Perubahan, Reset Password, Aktif/Nonaktif, Hapus User, Reset Form.
- Tabel: ID, Nama, Username, Role, Status.
- Username dikunci saat edit.
- Hapus user memerlukan konfirmasi.
- Akun yang sedang digunakan tidak dapat dihapus.
- Administrator aktif terakhir tidak dapat dihapus atau dinonaktifkan.

## Struktur Kasir PRO
- **Input Produk:** Barcode / Cari Produk, Qty, Tambah dan Cari Produk.
- **Keranjang Transaksi:** Barcode, Produk, Qty, Harga, Subtotal.
- **Kontrol Keranjang:** `− QTY`, `+ QTY`, `HAPUS ITEM`.
- **Pembayaran:** Total, Diskon, Metode, Bayar, Kembalian.
- **Kontrol Transaksi:** Parkir, Transaksi Parkir, Batal Transaksi, Riwayat dan Bayar & Cetak.
- Nilai transaksi/database tetap Decimal.
- Qty bulat pada struk ditampilkan tanpa `.0`.

## Produk
- Tambah, Edit, Nonaktifkan, Hapus aman.
- Produk dengan histori transaksi/mutasi tidak dapat dihapus permanen.
- Tabel Produk menampilkan: ID, Barcode, Nama, Kategori, Satuan, Beli, Jual, Stok, Status.
- Stok bulat ditampilkan tanpa pemisah desimal palsu, misalnya `20` bukan `20.000`.
- Status menunjukkan `AKTIF` atau `NONAKTIF`.

## CRUD Master
- Kategori: Tambah, Edit, Simpan, Hapus.
- Satuan: Tambah, Edit, Simpan, Hapus.
- Supplier: Tambah, Edit, Simpan, Hapus.
- Pelanggan: Tambah, Edit, Simpan, Hapus.

## Kasir
- Cari Produk berdasarkan nama/barcode.
- Scanner barcode + Enter.
- Qty − / +.
- Hapus item dan batal transaksi dengan konfirmasi.
- Diskon transaksi.
- Bayar dan Kembalian live.
- Pembayaran non-CASH mengikuti total.
- Riwayat dan cetak ulang struk.
- Parkir transaksi selama sesi aplikasi.
- Shortcut F4, F8, F9, F10 dan Escape.

## Reset Data
- **RESET TRANSAKSI & STOK** mempertahankan master bisnis.
- **RESET SEMUA DATA BISNIS** membersihkan master bisnis dan transaksi.
- User dan pengaturan toko dipertahankan.
- Konfirmasi wajib mengetik `RESET`.

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
- Administrator aktif terakhir tidak dapat dihapus atau dinonaktifkan.

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
Hasil utama: `dist\\WPOS PRO 2\\WPOS PRO 2.exe`.
EXE versioned: `dist\\WPOS_PRO_2_<APP_VERSION>.exe`.
SHA-256: file `.sha256.txt` di sebelah EXE versioned.

## Installer
Compile `installer.iss` menggunakan Inno Setup.
Output installer menggunakan nama `WPOS_PRO_2_Setup_<APP_VERSION>.exe`.

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
- Headerbar tiga zona: Context kiri, Nama Toko + Alamat tengah, Nama User + Tanggal kanan.
- Kasir menggunakan struktur Input Produk → Keranjang + Pembayaran → Kontrol Transaksi.
- Form Produk, Pembelian, Supplier dan Pelanggan menggunakan popup hybrid.
- Kategori dan Satuan menggunakan form inline/horizontal.
- Label dekoratif menggunakan background transparan secara global.
- Footer: **Nama aplikasi | Versi aplikasi | Tahun otomatis | by Jsuryana**.
- Login tidak mengulang versi aplikasi karena versi sudah tersedia di Footer.

## Excel Produk
- Export `.xlsx`.
- Template `.xlsx`.
- Import Tambah atau Update berdasarkan Barcode.
- Update tidak mengubah stok berjalan.

## Changelog
### 2.8.2
- Headerbar dibuat ownership-safe dengan memperbarui widget yang sudah ada.
- Dashboard Welcome tidak lagi menimpa context/hint Headerbar.
- Menambahkan regression test untuk mencegah reparenting widget Qt pada Headerbar.
- Menetapkan 2.8.2 sebagai PATCH release stabilisasi.

### 2.8.0
- Menambahkan field Nama user.
- Menambahkan edit user, hapus user dan perlindungan akun kritis.
- Menstandarkan role menjadi ADMIN/KASIR dan normalisasi role legacy TEKNISI.
- Menambahkan tabel Manajemen User lima kolom.
- Menetapkan 2.8.0 sebagai MINOR release.

### 2.7.17
- Menerapkan global UI rule untuk membuat background label dekoratif transparan.
- Menghilangkan visual box inside box yang tidak diperlukan.
- Mempertahankan background komponen fungsional.
- Tidak mengubah business logic, schema/database atau authentication flow.

### 2.7.16
- Hardening Backup / Restore SQLite.
- Backup restore sekarang menolak file yang corrupt atau tidak memiliki tabel inti yang diperlukan.
