# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.11.1**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Perubahan terbaru 2.11.1
- Memperkuat keamanan bootstrap Administrator dengan **wajib ganti password** ketika akun `admin` masih menggunakan password awal `admin123`.
- Password baru Administrator minimal 8 karakter dan tetap disimpan menggunakan PBKDF2-SHA256 dengan salt acak.
- Perubahan ini mempertahankan kompatibilitas database existing dan hanya memaksa perubahan saat credential bootstrap lama masih aktif.
- Memperbaiki **CI regression contract** setelah security hardening: test identitas aplikasi kini memvalidasi format SemVer dari `APP_VERSION`, sehingga patch release `2.11.1` tidak mematahkan test yang mengunci versi lama.
- Mempertahankan contract import login pada `app/ui/login.py` agar regression test tetap dapat memverifikasi jalur autentikasi setelah penambahan forced password change.
- Release publisher sekarang menggunakan repository secret **`WPOS_RELEASE_TOKEN`** untuk autentikasi GitHub CLI, menggantikan `github.token` yang sebelumnya ditolak GitHub dengan HTTP 403 saat membuat Release.
- Menambahkan validasi awal bahwa release token tersedia dan dapat mengakses repository sebelum artifact/release diproses.
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

## Perubahan terbaru 2.10.0
- Menerapkan pemisahan akses role **ADMIN** dan **KASIR** pada navigasi aplikasi.
- ADMIN tetap memiliki akses penuh ke seluruh 14 halaman dan Manajemen User.
- KASIR dibatasi pada **Dashboard, Kasir, dan Pelanggan** sesuai policy permission yang sudah ada.
- Menyembunyikan halaman yang tidak berhak diakses KASIR dari sidebar.
- Menambahkan runtime guard pada jalur navigasi compatibility/legacy agar halaman terlarang tidak dapat dibuka melalui `setCurrentIndex()`.
- Menjadikan mapping page → permission terpusat pada layer access control UI.
- Menambahkan regression test untuk mapping 14 halaman dan perbedaan akses ADMIN/KASIR.
- Tidak mengubah login UI, business logic transaksi, database transaksi, receipt thermal, atau workflow multi-item purchase.
- Release **2.10.0** dikategorikan sebagai MINOR karena menambahkan kontrol akses role-based yang backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.
