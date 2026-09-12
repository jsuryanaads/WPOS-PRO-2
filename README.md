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
