# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.9.0**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Perubahan terbaru 2.9.0
- Menambahkan **multi-item purchase** pada menu **Pembelian**.
- Satu invoice pembelian sekarang dapat berisi banyak produk dalam satu transaksi.
- Menambahkan keranjang item pembelian dengan produk, barcode, qty, harga beli, subtotal, dan aksi hapus per baris.
- Item produk yang sama pada keranjang digabung: qty ditambahkan dan harga beli diperbarui ke input terakhir.
- Menampilkan jumlah item dan **TOTAL PEMBELIAN** secara realtime sebelum disimpan.
- Supplier dan nomor invoice berlaku untuk seluruh item dalam satu transaksi pembelian.
- Nomor invoice tetap dibuat otomatis jika field invoice dikosongkan.
- Penyimpanan tetap menggunakan `create_purchase()` sehingga validasi, stok, PurchaseItem, dan StockMovement tetap berada di service layer.
- Setelah pembelian berhasil, tampilan Produk dan Stok & Mutasi direfresh agar stok terbaru langsung terlihat.
- Tidak mengubah schema database karena backend `Purchase` → `PurchaseItem` sebelumnya sudah mendukung banyak item.
- Release **2.9.0** dikategorikan sebagai MINOR karena menambahkan fungsi multi-item pada UI secara backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

## Perubahan terbaru 2.8.6
- Merapikan **Ringkasan Pembayaran** pada halaman Kasir agar lebih compact dan proporsional.
- Menghilangkan ruang kosong vertikal berlebihan pada panel pembayaran.
- Panel pembayaran mengikuti tinggi konten dan tetap sejajar di bagian atas dengan area keranjang.
- Menjaga hierarchy visual: TOTAL paling dominan, field pembayaran tetap mudah digunakan, dan Kembalian tetap menjadi hasil utama kedua.
- Kontrol transaksi tetap berada di area khusus **Kontrol Transaksi**.
- Tidak mengubah business logic checkout, perhitungan total, metode pembayaran, stok, database, atau fungsi cetak.
- Release **2.8.6** dikategorikan sebagai PATCH karena merupakan penyempurnaan UI backward-compatible.

## Perubahan terbaru 2.8.5
- Menambahkan **Kasir: <Nama User>** pada receipt/struk.
- Nama kasir diambil dari `User.name` milik user yang sedang login, bukan username.
- Jika nama user kosong, receipt menggunakan fallback **Pengguna**.
- Diterapkan pada renderer Qt/HTML dan RAW ESC/POS, termasuk test print.
- Posisi Kasir ditempatkan setelah tanggal transaksi dan sebelum separator/item.
- Tidak mengubah perhitungan transaksi, database transaksi, atau payment logic.
- Release **2.8.5** dikategorikan sebagai PATCH karena merupakan penyempurnaan receipt backward-compatible.

## Perubahan terbaru 2.8.4
- Memposisikan **nama toko + alamat toko** tepat di tengah geometris Headerbar.
- Headerbar menggunakan tiga zona dengan stretch seimbang: kiri untuk judul/hint, tengah untuk identitas toko, kanan untuk user/tanggal.
- Perubahan posisi dilakukan tanpa `setParent(None)`, `layout.removeItem`, atau reparenting widget Qt.
- Menambahkan regression test untuk memastikan zona Headerbar tetap true-centered.
- Tidak mengubah business logic, database, authentication, transaksi, atau struktur 14 halaman.
- Release **2.8.4** dikategorikan sebagai PATCH karena merupakan penyempurnaan UI backward-compatible.

## Perubahan terbaru 2.8.3
- Menghilangkan label **Admin** dan **ADMIN · Lokal** dari area sidebar di atas tombol **Keluar**.
- Identitas pengguna tetap ditampilkan di **Headerbar kanan** sebagai nama display user + tanggal Indonesia.
- Sidebar sekarang fokus pada navigasi dan tombol Keluar tanpa duplikasi identitas pengguna.
- Perubahan hanya UI; business logic, database, authentication, transaksi, dan 14 halaman tetap dipertahankan.
- Release **2.8.3** dikategorikan sebagai PATCH karena merupakan bug fix UI backward-compatible.

## Perubahan terbaru 2.8.2
- Memperbaiki Headerbar agar update dilakukan pada widget yang sudah ada tanpa `setParent(None)` atau `layout.removeItem`.
- Menjaga ownership/lifetime widget Qt tetap stabil saat UI direfresh atau berpindah halaman.
- Headerbar menampilkan **judul + hint halaman aktif** di kiri, **nama toko + alamat toko** di tengah, dan **nama display user + tanggal Indonesia** di kanan.
- `Dashboard Welcome` tidak lagi menimpa Headerbar global dengan username atau tanggal legacy.
- Menambahkan regression test untuk kontrak Headerbar ownership-safe dan pemisahan Dashboard.
- Tidak mengubah business logic transaksi, database, authentication, atau struktur 14 halaman.
- Release **2.8.2** dikategorikan sebagai PATCH karena merupakan bug fix/hardening backward-compatible.

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
│ KASIR                    TOKO SEMBAKO SAPNI                 Admin           │
│ Transaksi cepat · barcode first                         12 September 2026   │
│                              Alamat Toko                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```
- **Kiri:** judul halaman aktif + subtitle/hint dinamis; berubah mengikuti halaman yang dipilih.
- **Tengah:** nama toko + alamat toko dari `Pengaturan Toko`, selalu diposisikan center.
- **Kanan:** username pengguna yang sedang login + tanggal otomatis dalam format Indonesia.
- Username tidak ditampilkan di zona tengah.
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

## Pembelian PRO
- **Informasi Pembelian:** Supplier dan No. Invoice.
- **Tambah Item:** Produk, Qty, Harga Beli, Tambah Item.
- **Keranjang Pembelian:** Produk, Barcode, Qty, Harga Beli, Subtotal, Hapus.
- Satu invoice dapat berisi banyak produk.
- Produk yang sama dalam keranjang digabung dengan penambahan Qty dan harga beli terakhir.
- **TOTAL PEMBELIAN** dihitung realtime.
- Penyimpanan satu invoice tetap atomic melalui service `create_purchase()`.
- Setiap item menghasilkan `PurchaseItem` dan `StockMovement` sesuai service layer.

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
