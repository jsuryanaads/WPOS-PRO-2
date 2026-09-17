# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.13.1**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

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
- Release automation sekarang memiliki **wait/poll gate** untuk menunggu Windows Installer selesai sebelum artifact dicari, sehingga publish tidak race-condition dengan build pipeline.
- Release **2.13.0** dikategorikan sebagai MINOR karena merupakan redesign presentation layer yang backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

## Perubahan terbaru 2.12.0
- Memperkenalkan **Responsive + Realtime Premium UI** sebagai presentation layer tanpa mengubah business logic, database, authentication, transaksi, stok, atau printer.
- Layout Modern Shell menyesuaikan lebar jendela secara dinamis, termasuk sidebar, panel pembayaran Kasir, margin halaman, dan ruang konten.
- Menambahkan refresh dashboard ringan setiap 3 detik agar KPI dan tabel ringkasan mengikuti perubahan data lokal tanpa restart atau pindah halaman.
- Refresh realtime bersifat fail-safe: kegagalan refresh presentation tidak boleh mengganggu sesi POS atau transaksi aktif.
- Mempertahankan Premium UI System, Dark/Light Mode, keyboard workflow, dan struktur halaman existing.
- Fokus desain: modern retail untuk pengguna Gen Z dan Milenial, dengan hierarchy visual yang lebih fluid dan mengurangi kesan UI administratif yang kaku.
- Memperkuat **release publisher** agar mencari Windows Installer yang sukses berdasarkan `TARGET_SHA` secara dinamis, bukan mengunci `BUILD_RUN_ID` yang mudah stale pada release berikutnya.
- Menambahkan validation gate bahwa run installer yang dipilih benar-benar sukses dan memiliki artifact release yang belum expired sebelum proses upload/publish dijalankan.
- Release **2.12.0** dikategorikan sebagai MINOR karena merupakan penyempurnaan UI lintas aplikasi yang backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

## Perubahan terbaru 2.11.1
- Memperkuat keamanan bootstrap Administrator dengan **wajib ganti password** ketika akun `admin` masih menggunakan password awal `admin123`.
- Password baru Administrator minimal 8 karakter dan tetap disimpan menggunakan PBKDF2-SHA256 dengan salt acak.
- Perubahan ini mempertahankan kompatibilitas database existing dan hanya memaksa perubahan saat credential bootstrap lama masih aktif.
- Memperbaiki **CI regression contract** setelah security hardening: test identitas aplikasi kini memvalidasi format SemVer dari `APP_VERSION`, sehingga patch release `2.11.1` tidak mematahkan test yang mengunci versi lama.
- Mempertahankan contract import login pada `app/ui/login.py` agar regression test tetap dapat memverifikasi jalur autentikasi setelah penambahan forced password change.
- Release publisher sekarang menggunakan repository secret **`WPOS_RELEASE_TOKEN`** untuk autentikasi GitHub CLI, menggantikan `github.token` yang sebelumnya ditolak GitHub dengan HTTP 403 saat membuat Release.
- Menambahkan validasi awal bahwa release token tersedia dan dapat mengakses repository sebelum artifact/release diproses.
- Menambahkan diagnostik eksplisit sebelum pembuatan draft Release agar target tag dan SHA release terlihat di log Actions saat troubleshooting.
- Tidak ada perubahan versi karena perbaikan ini merupakan stabilisasi release automation di dalam release **2.11.1**.
- Release **2.11.1** dikategorikan sebagai PATCH karena merupakan security hardening dan stabilisasi release automation yang backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

## Perubahan terbaru 2.11.0
- Menerapkan **Premium UI System** secara global pada seluruh halaman aplikasi, bukan hanya Dashboard/Kasir.
- Menstandarkan hierarchy visual, spacing, radius, tinggi kontrol, tabel, form field, tombol, dialog, tooltip, dan scrollbar.
- Memperhalus **sidebar, brand panel, navigation state, account panel, topbar, dan content surface** pada Modern Shell.
- Menambahkan state visual hover, pressed, selected, focus, dan disabled agar interaksi lebih jelas.
- Memperkuat keterbacaan tabel dan form dengan header, row hover, focus ring, dan surface hierarchy yang konsisten.
- Menyempurnakan Dark Mode dan Light Mode tanpa mengubah business logic, database, authentication, transaksi, stok, atau receipt.
- Menyelaraskan label tombol **Simpan Pembelian & Tambah Stok** dengan UI contract/regression test tanpa mengubah alur transaksi pembelian.
- Release **2.11.0** dikategorikan sebagai MINOR karena merupakan penyempurnaan UI lintas aplikasi yang backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

## Perubahan terbaru 2.10.1
- Memperbaiki bug **multi-item purchase**: produk yang sama dengan harga beli berbeda tidak lagi digabung menjadi satu baris dengan harga terakhir.
- Memperbaiki workflow **Kasir** ketika transaksi berhasil tersimpan tetapi proses cetak struk mengalami exception: transaksi tetap dilaporkan berhasil dan kegagalan cetak ditampilkan sebagai status cetak, bukan sebagai kegagalan transaksi.
- Mencegah **ADMIN aktif melakukan self-demotion** dari ADMIN menjadi KASIR pada sesi yang sedang berjalan, sehingga privilege sesi tidak tertinggal berbeda dari role yang dimaksudkan.
- Release **2.10.1** dikategorikan sebagai PATCH karena berisi bug fix dan security hardening yang backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.
