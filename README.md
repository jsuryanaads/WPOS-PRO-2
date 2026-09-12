# WPOS PRO 2

Modern POS desktop untuk toko sembako Windows offline, satu komputer.

## Identitas
- Nama aplikasi: **WPOS PRO 2**
- Versi aplikasi: **2.8.3**
- Platform: Windows
- Mode: Offline / database lokal
- Database: SQLite

## Perubahan terbaru 2.8.3
- Menghilangkan label **Admin** dan **ADMIN · Lokal** dari area sidebar di atas tombol **Keluar**.
- Identitas pengguna tetap ditampilkan di **Headerbar kanan** sebagai nama display user + tanggal Indonesia.
- Sidebar sekarang fokus pada navigasi dan tombol Keluar tanpa duplikasi identitas pengguna.
- Perubahan hanya UI; business logic, database, authentication, transaksi, dan 14 halaman tetap dipertahankan.
- Release **2.8.3** dikategorikan sebagai PATCH karena merupakan bug fix UI backward-compatible.
- Setiap perubahan versi dicatat di README dan Changelog.

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
