# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.11.0**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

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

## Perubahan terbaru 2.9.3
- Memperbaiki formatter item pada receipt thermal 58mm agar Qty integral seperti `1.0` dicetak sebagai `1`.
- Memperbaiki perhitungan lebar baris item agar dua separator tidak ikut memakan ruang nominal terakhir.
- Mencegah nominal item seperti `30,000` terpotong menjadi `30,00` pada printer 32-CPL.
- Memperbarui renderer Qt/HTML agar Qty juga menggunakan formatter receipt yang sama.
- Menambahkan regression test untuk Qty, panjang baris 32 karakter, dan nominal item yang tidak terpotong.
- Tidak mengubah business logic transaksi, perhitungan Decimal, database, pembayaran, stok, atau workflow multi-item purchase.
- Release **2.9.3** dikategorikan sebagai PATCH karena merupakan bug fix receipt backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

## Perubahan terbaru 2.9.2
- Memperbaiki **Ringkasan Pembayaran** pada halaman Kasir agar label nilai tidak kembali menjadi `TOTAL Rp ...` dan `Kembalian: Rp ...` setelah cart/payment di-refresh.
- Menambahkan runtime contract pada layer UI Kasir untuk mempertahankan format dua baris: caption dan value.
- Regression test sekarang memverifikasi bahwa contract runtime tersebut tetap terpasang.
- Tidak mengubah business logic checkout, perhitungan total, metode pembayaran, stok, database, atau workflow multi-item purchase.
- Release **2.9.2** dikategorikan sebagai PATCH karena merupakan bug fix UI backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.
