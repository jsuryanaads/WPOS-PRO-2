# WPOS PRO 2 Changelog

## 2.11.1 — Bootstrap Admin Security Hardening

- Memperkuat keamanan bootstrap Administrator dengan **wajib ganti password** ketika akun `admin` masih menggunakan password awal `admin123`.
- Password baru Administrator minimal 8 karakter dan tetap disimpan menggunakan PBKDF2-SHA256 dengan salt acak.
- Perubahan mempertahankan kompatibilitas database existing dan hanya memaksa perubahan saat credential bootstrap lama masih aktif.
- Menambahkan helper terpisah untuk mendeteksi credential bootstrap dan mengganti password dengan policy hashing aplikasi.
- Menetapkan **2.11.1** sebagai PATCH release untuk security hardening backward-compatible.

## 2.11.0 — Premium UI System

- Menerapkan **Premium UI System** secara global pada seluruh halaman aplikasi.
- Menstandarkan hierarchy visual, spacing, radius, tinggi kontrol, tabel, form field, tombol, dialog, tooltip, dan scrollbar.
- Memperhalus **sidebar, brand panel, navigation state, account panel, topbar, dan content surface** pada Modern Shell.
- Menambahkan state visual hover, pressed, selected, focus, dan disabled agar interaksi lebih jelas.
- Memperkuat keterbacaan tabel dan form dengan header, row hover, focus ring, dan surface hierarchy yang konsisten.
- Menyempurnakan Dark Mode dan Light Mode.
- Tidak mengubah business logic, database, authentication, transaksi, stok, atau receipt.
- Menetapkan **2.11.0** sebagai MINOR release karena merupakan penyempurnaan UI lintas aplikasi yang backward-compatible.

## 2.10.1 — Production Bug Fix & Hardening

- Memperbaiki bug **multi-item purchase**: produk yang sama dengan harga beli berbeda tidak lagi digabung menjadi satu baris dengan harga terakhir.
- Memperbaiki workflow **Kasir** ketika transaksi berhasil tersimpan tetapi proses cetak struk mengalami exception: transaksi tetap dilaporkan berhasil dan kegagalan cetak tidak dianggap sebagai kegagalan transaksi.
- Mencegah **ADMIN aktif melakukan self-demotion** dari ADMIN menjadi KASIR pada sesi yang sedang berjalan.
- Menetapkan **2.10.1** sebagai PATCH release untuk bug fix dan security hardening backward-compatible.

## 2.10.0 — Role-Based Access Control

- Menerapkan pemisahan akses role **ADMIN** dan **KASIR** pada navigasi aplikasi.
- ADMIN memiliki akses penuh ke seluruh 14 halaman dan Manajemen User.
- KASIR dibatasi pada **Dashboard, Kasir, dan Pelanggan** sesuai `ROLE_PERMISSIONS` yang sudah menjadi policy aplikasi.
- Menyembunyikan item navigasi yang tidak diizinkan untuk role aktif.
- Menyembunyikan section navigasi yang seluruh isinya tidak tersedia untuk role aktif.
- Menambahkan runtime guard pada compatibility/legacy navigation agar `setCurrentIndex()` tidak dapat membuka halaman terlarang.
- Menjadikan mapping page index → permission feature terpusat pada `app/ui/access_control.py`.
- Menambahkan regression test untuk coverage 14 halaman serta perbedaan akses ADMIN/KASIR.
- Tidak mengubah login UI, business logic transaksi, database transaksi, receipt thermal, atau workflow multi-item purchase.
- Menetapkan **2.10.0** sebagai MINOR release karena menambahkan functionality role-based access yang backward-compatible.

## Release rule

WPOS PRO 2 uses Semantic Versioning (`MAJOR.MINOR.PATCH`):

- **PATCH**: bug fixes, hardening, and backward-compatible stabilization.
- **MINOR**: new backward-compatible functionality.
- **MAJOR**: breaking changes or incompatible architecture/API changes.

A version is a release milestone, not a commit counter. A release is considered complete only when the source version, installer version, build artifacts, tests, and release metadata are consistent.
