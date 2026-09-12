# WPOS PRO 2 Changelog

## 2.9.2 — Cashier Payment Label Runtime Fix

- Memperbaiki runtime halaman **Kasir** yang sebelumnya menimpa label compact menjadi `TOTAL Rp ...` dan `Kembalian: Rp ...` setiap kali cart/payment di-refresh.
- Menambahkan runtime contract pada `cashier_structure` sehingga nilai tetap ditampilkan pada dua baris: caption dan value.
- Menambahkan regression test untuk memastikan contract wrapper `update_change()` tetap terpasang.
- Tidak mengubah business logic checkout, perhitungan total, metode pembayaran, stok, database, atau workflow multi-item purchase.
- Menetapkan **2.9.2** sebagai PATCH release untuk bug fix UI backward-compatible.

## 2.9.1 — Receipt Print-Safe Refinement

- Menambahkan **print-safe top area** pada struk thermal 58mm agar nama toko tidak terlalu dekat dengan tepi fisik kertas.
- Menambahkan dua blank feed line pada jalur RAW ESC/POS setelah inisialisasi printer.
- Menambahkan top padding 2mm pada renderer Qt/HTML tanpa mengubah lebar cetak 48mm.
- Mempertahankan format Qty bulat tanpa `.0` pada tampilan struk; nilai transaksi tetap menggunakan Decimal.
- Menambahkan helper terpisah untuk formatting output receipt tanpa mencampur business logic transaksi.
- Tidak mengubah database, stok, pembayaran, checkout, atau workflow multi-item purchase.
- Menetapkan **2.9.1** sebagai PATCH release untuk penyempurnaan output receipt backward-compatible.

## 2.9.0 — Multi-Item Purchase

- Menambahkan workflow **multi-item** pada menu **Pembelian**.
- Satu invoice pembelian dapat memuat banyak produk dalam satu keranjang sebelum disimpan.
- Menambahkan kolom Produk, Barcode, Qty, Harga Beli, Subtotal, dan aksi Hapus.
- Produk yang sama digabung ke baris yang sama: Qty ditambahkan dan harga beli mengikuti input terakhir.
- Menampilkan jumlah item dan total pembelian secara realtime.
- Supplier dan nomor invoice digunakan untuk seluruh item dalam satu purchase.
- Nomor invoice otomatis tetap tersedia jika field invoice dikosongkan.
- Penyimpanan tetap didelegasikan ke `create_purchase()` sehingga aturan transaksi dan stock movement tidak diduplikasi di UI.
- Tidak memerlukan perubahan schema database karena model `Purchase` dan `PurchaseItem` sudah mendukung relasi satu purchase ke banyak item.
- Menambahkan regression test untuk kontrak UI dan sinkronisasi versi.
- Menetapkan **2.9.0** sebagai MINOR release karena menambahkan functionality backward-compatible.

## 2.8.6 — Compact Payment Summary

- Merapikan **Ringkasan Pembayaran** pada halaman Kasir agar lebih compact dan proporsional.
- Menghilangkan ruang kosong vertikal berlebihan pada panel pembayaran.
- Panel pembayaran mengikuti tinggi konten dan menggunakan size policy maksimum secara vertikal.
- Memperketat spacing internal agar TOTAL, Diskon, Metode, Bayar, dan Kembalian memiliki hierarchy yang jelas.
- Area **Kontrol Transaksi** tetap dipisahkan dari ringkasan pembayaran.
- Tidak mengubah business logic checkout, perhitungan total, metode pembayaran, stok, database, atau fungsi cetak.
- Menetapkan **2.8.6** sebagai PATCH release untuk penyempurnaan UI backward-compatible.

## 2.8.5 — Cashier Name on Receipt

- Menambahkan **Kasir: <Nama User>** pada receipt/struk.
- Nama kasir bersumber dari `User.name` user yang sedang login, bukan username.
