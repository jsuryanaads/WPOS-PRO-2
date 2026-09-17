# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.13.2**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Perubahan terbaru 2.13.2
- Memperbarui halaman Printer menjadi **Printer Center** dengan layout card yang lebih profesional.
- Memisahkan konfigurasi **Printer Struk Thermal 58mm** dan **Printer Laporan A4 Portrait**.
- Menambahkan **Cetak Laporan A4** dari halaman Laporan dengan ringkasan dan tabel transaksi terakhir.
- Menambahkan service `report_printer` khusus laporan agar konfigurasi A4 tidak mengubah profil receipt 58mm.
- Memperbaiki refresh printer agar tidak membuat ulang halaman/tab Printer.
- Business logic transaksi, database, authentication, stok, dan receipt thermal tetap dipertahankan.
- Release **2.13.2** dikategorikan sebagai PATCH karena merupakan penyempurnaan printer/report yang backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

## Perubahan terbaru 2.13.1
- Memperbarui halaman Login menjadi fullscreen, responsive, dan premium tanpa mengubah authentication flow atau business logic.
- Menggunakan background PNG branding edge-to-edge dengan glass/translucent login card dan responsive positioning.
- Menambahkan/menjaga kontrol Login, password toggle, tombol keluar, logo, dan footer dalam layout yang adaptif.
- Mempertahankan jalur autentikasi, database session, forced password change, dan contract regression existing.
- Release **2.13.1** dikategorikan sebagai PATCH karena merupakan penyempurnaan presentation layer yang backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

## Perubahan terbaru 2.13.0
- Mengganti pendekatan responsive yang sebelumnya terlalu subtle dengan **Visible Premium UI Refresh** yang benar-benar mengubah hierarchy visual pada shell dan halaman bisnis.
- Modern Shell kini menggunakan sidebar yang lebih tegas, topbar lebih lapang, navigation state lebih jelas, card KPI lebih besar, surface lebih berlapis, border/radius lebih modern, dan tombol dengan state interaksi yang lebih nyata.
- Dashboard KPI memakai card hierarchy baru dengan shadow, typography lebih kuat, spacing lebih lega, dan table density yang lebih nyaman untuk penggunaan POS harian.
- Kasir mendapatkan visual scan/search area yang lebih menonjol, payment panel lebih kuat secara hierarchy, total/kembalian lebih mudah dipindai, serta tombol checkout yang memiliki emphasis khusus.
- Seluruh tabel, form input, group box, scrollbar, navigation, dan action button mengikuti visual contract baru agar perubahan terasa lintas aplikasi, bukan hanya pada satu halaman.
- Responsive behavior memakai breakpoint nyata untuk sidebar, topbar, content margin, dan panel pembayaran sehingga layout tetap usable pada ukuran jendela yang berbeda.
- Realtime dashboard tetap berjalan setiap 3 detik dengan fail-safe agar refresh presentation tidak mengganggu transaksi.
- Business logic, database, authentication, stok, transaksi, dan printer tidak diubah oleh visual layer ini.
- Release automation memiliki **wait/poll gate** untuk menunggu Windows Installer selesai sebelum artifact dicari.
- Release **2.13.0** dikategorikan sebagai MINOR karena merupakan redesign presentation layer yang backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

## Perubahan terbaru 2.12.0
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
