# WPOS PRO 2 Changelog

## 2.8.5 — Cashier Name on Receipt

- Menambahkan **Kasir: <Nama User>** pada receipt/struk.
- Nama kasir bersumber dari `User.name` user yang sedang login, bukan username.
- Jika `User.name` kosong, digunakan fallback **Pengguna**.
- Diterapkan pada renderer Qt/HTML dan RAW ESC/POS, termasuk test print.
- Posisi Kasir berada setelah tanggal transaksi dan sebelum separator/item.
- Tidak mengubah perhitungan transaksi, database transaksi, atau payment logic.
- Menetapkan **2.8.5** sebagai PATCH release untuk penyempurnaan receipt backward-compatible.

## 2.8.4 — True-Centered Headerbar

- Memposisikan **nama toko + alamat toko** tepat di tengah geometris Headerbar.
- Headerbar menggunakan tiga zona dengan stretch seimbang: kiri untuk judul/hint, tengah untuk identitas toko, kanan untuk user/tanggal.
- Perubahan posisi dilakukan tanpa `setParent(None)`, `layout.removeItem`, atau reparenting widget Qt.
- Menambahkan regression test untuk memastikan zona Headerbar tetap true-centered.
- Tidak mengubah business logic, database, authentication, transaksi, atau struktur 14 halaman.
- Menetapkan **2.8.4** sebagai PATCH release untuk penyempurnaan UI backward-compatible.

## 2.8.3 — Sidebar Account Cleanup

- Menghilangkan label **Admin** dan **ADMIN · Lokal** dari area sidebar yang berada tepat di atas tombol **Keluar**.
- Identitas pengguna tetap ditampilkan pada Headerbar kanan sesuai desain global: nama display user + tanggal Indonesia.
- Sidebar kini berfokus pada navigasi dan tombol Keluar tanpa duplikasi identitas pengguna.
- Perubahan hanya bersifat UI dan tidak mengubah business logic, database, authentication, transaksi, atau struktur halaman.
- Menetapkan **2.8.3** sebagai PATCH release untuk perbaikan UI backward-compatible.

## 2.8.2 — Headerbar Stabilization

- Memperbaiki Headerbar agar tidak melakukan `setParent(None)`, `layout.removeItem`, atau reparenting widget Qt saat refresh.
- Menjaga ownership/lifetime widget Qt tetap stabil dengan memperbarui QLabel yang sudah ada di tempatnya.
- Headerbar sekarang menampilkan nama toko + alamat toko di tengah dan nama display user + tanggal Indonesia di kanan tanpa mengganti struktur layout saat runtime.
- `Dashboard Welcome` tidak lagi menimpa context/hint Headerbar global dengan username atau tanggal legacy.
- Menambahkan regression test untuk kontrak ownership-safe Headerbar dan pemisahan tanggung jawab Dashboard.
- Tidak mengubah business logic transaksi, database, authentication, atau struktur 14 halaman.
- Menetapkan **2.8.2** sebagai PATCH release stabilisasi.

## 2.8.0 — User Management & Account Administration

- Menambahkan field **Nama** pada akun user sehingga identitas user tidak hanya bergantung pada username.
- Menambahkan fitur **Simpan Perubahan** untuk mengubah nama, role, dan status user.
- Menambahkan fitur **Hapus User** dengan konfirmasi sebelum penghapusan permanen.
- Melindungi akun yang sedang digunakan agar tidak dapat dihapus sendiri.
- Melindungi Administrator aktif terakhir agar tidak dapat dihapus atau dinonaktifkan sehingga sistem selalu memiliki minimal satu Administrator aktif.
- Mengunci field username saat mode edit untuk mencegah perubahan identitas login secara tidak sengaja.
- Menstandarkan role aplikasi menjadi `ADMIN` dan `KASIR`; data role legacy `TEKNISI` dinormalisasi menjadi `KASIR` saat migrasi user.
- Menambahkan regression coverage untuk kontrak role dan manajemen akun.
- Memperbarui UI Manajemen User menjadi tabel lima kolom: ID, Nama, Username, Role, Status.
- Menetapkan **2.8.0** sebagai MINOR release karena menambahkan functionality backward-compatible serta perubahan schema user yang diperlukan untuk fitur Nama.

## 2.7.17 — Global UI Refinement

- Applied a global UI rule across all 14 business pages: decorative label backgrounds are transparent by default.
- Removed the visual "box inside box" treatment caused by unnecessary label backgrounds while preserving functional backgrounds for inputs, buttons, tables, cards, badges, and panels.
- Standardized label presentation so text sits directly on its parent surface unless a specific component requires its own background.
- Kept business logic, database schema, authentication flow, and transaction behavior unchanged.
- Recorded the version change in README and Changelog according to the release versioning policy.

## 2.7.16 — Stabilization Release

- Strengthened SQLite backup restore validation.
- Added integrity and core-schema validation before restoring a database.
- Added a safety backup of the active database before restore replacement.
- Added automated backup/restore regression coverage.
- Enforced SemVer validation in the Windows build pipeline.
- Aligned installer metadata with application version `2.7.16`.
- Versioned EXE and installer artifacts by release version.
- Added SHA-256 checksum generation for the installer artifact.
- Updated the local Windows build script to run compile checks and tests before packaging.

### Release rule

WPOS PRO 2 uses Semantic Versioning (`MAJOR.MINOR.PATCH`):

- **PATCH**: bug fixes, hardening, and backward-compatible stabilization.
- **MINOR**: new backward-compatible functionality.
- **MAJOR**: breaking changes or incompatible architecture/API changes.

A version is a release milestone, not a commit counter. A release is considered complete only when the source version, installer version, build artifacts, tests, and release metadata are consistent.