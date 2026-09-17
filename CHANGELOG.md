# WPOS PRO 2 Changelog

## 2.13.2 — Printer Center & A4 Report Printing

- Memperbarui halaman Printer menjadi **Printer Center** dengan layout card yang lebih profesional dan pemisahan konfigurasi printer yang jelas.
- Mempertahankan profil **struk thermal 58mm** tanpa perubahan pada konfigurasi receipt existing.
- Menambahkan konfigurasi printer **laporan A4 Portrait** yang terpisah dari printer struk.
- Menambahkan aksi **Cetak Laporan A4** dari halaman Laporan.
- Laporan A4 mencakup ringkasan laporan dan tabel transaksi terakhir.
- Memisahkan service `report_printer` dari service receipt agar profil A4 tidak mencampur atau mengubah setting thermal 58mm.
- Memperbaiki refresh daftar printer agar hanya memperbarui pilihan printer tanpa membuat ulang halaman/tab Printer.
- Tidak mengubah business logic transaksi, database, authentication, stok, atau alur struk thermal.
- Menetapkan **2.13.2** sebagai PATCH release karena merupakan penyempurnaan printer/report yang backward-compatible.

## 2.13.1 — Premium Login UI

- Memperbarui halaman Login menjadi fullscreen, responsive, dan premium tanpa mengubah authentication flow atau business logic.
- Menggunakan background PNG branding edge-to-edge dengan glass/translucent login card dan responsive positioning.
- Menambahkan/menjaga kontrol Login, password toggle, tombol keluar, logo, dan footer dalam layout yang adaptif.
- Mempertahankan jalur autentikasi, database session, forced password change, dan contract regression existing.
- Menetapkan **2.13.1** sebagai PATCH release karena merupakan penyempurnaan presentation layer yang backward-compatible.

## 2.13.0 — Visible Premium UI Refresh

- Mengganti responsive layer yang sebelumnya terlalu subtle dengan **Visible Premium UI Refresh** agar perubahan visual benar-benar terasa saat aplikasi dijalankan.
- Memperkuat Modern Shell melalui sidebar, topbar, navigation state, content surface, card KPI, typography, border, radius, spacing, dan interaction states yang lebih modern.
- Menambahkan hierarchy visual baru pada Dashboard, termasuk KPI cards dengan shadow dan table density yang lebih nyaman.
- Memperkuat visual halaman Kasir pada scan/search area, cart surface, payment panel, total/kembalian, dan tombol checkout.
- Menstandarkan visual table, form input, group box, scrollbar, dan action button lintas halaman.
- Menambahkan breakpoint responsive yang lebih nyata untuk sidebar, topbar, content margin, dan payment panel.
- Mempertahankan realtime dashboard refresh setiap 3 detik dengan fail-safe presentation behavior.
- Tidak mengubah business logic, database, authentication, stok, transaksi, atau printer.
- Menetapkan **2.13.0** sebagai MINOR release karena merupakan redesign presentation layer yang backward-compatible.

## 2.12.0 — Responsive + Realtime Premium UI

- Memperkenalkan **Responsive + Realtime Premium UI** sebagai presentation layer tanpa mengubah business logic, database, authentication, transaksi, stok, atau printer.
- Layout Modern Shell menyesuaikan lebar jendela secara dinamis, termasuk sidebar, panel pembayaran Kasir, margin halaman, dan ruang konten.
- Menambahkan refresh dashboard ringan setiap 3 detik agar KPI dan tabel ringkasan mengikuti perubahan data lokal tanpa restart atau pindah halaman.
- Refresh realtime bersifat fail-safe: kegagalan refresh presentation tidak mengganggu sesi POS atau transaksi aktif.
- Mempertahankan Premium UI System, Dark/Light Mode, keyboard workflow, dan struktur halaman existing.
- Mengarahkan visual ke modern retail yang lebih fluid dan mengurangi kesan UI administratif yang kaku.
- Memperkuat release publisher agar mencari Windows Installer yang sukses berdasarkan `TARGET_SHA` secara dinamis, bukan mengunci `BUILD_RUN_ID` yang mudah stale.
- Menambahkan validation gate bahwa run installer yang dipilih benar-benar sukses dan memiliki artifact release yang belum expired.

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

## 2.9.2 — Cashier Payment Label Runtime Fix

- Memperbaiki runtime halaman **Kasir** agar label pembayaran tetap konsisten setelah halaman dibuat ulang atau diperbarui.
- Menjaga label dan state pembayaran tetap sinkron dengan alur transaksi Kasir.
- Menambahkan regression test untuk memastikan fix runtime tetap terdokumentasi dan terlindungi dari regresi.

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
