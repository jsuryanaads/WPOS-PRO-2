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
- Memperkuat release publisher agar mencari Windows Installer yang sukses berdasarkan `TARGET_SHA` secara dinamis, bukan mengunci `BUILD_RUN_ID` yang mudah stale.
- Menambahkan validation gate bahwa run installer yang dipilih benar-benar sukses dan memiliki artifact release yang belum expired.

## Release rule

WPOS PRO 2 uses Semantic Versioning (`MAJOR.MINOR.PATCH`):

- **PATCH**: bug fixes, hardening, and backward-compatible stabilization.
- **MINOR**: new backward-compatible functionality.
- **MAJOR**: breaking changes or incompatible architecture/API changes.

A version is a release milestone, not a commit counter. A release is considered complete only when the source version, installer version, build artifacts, tests, and release metadata are consistent.
