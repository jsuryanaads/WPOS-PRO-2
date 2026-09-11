from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView, QDialog, QDialogButtonBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QPushButton, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QDoubleSpinBox, QComboBox, QWidget,
)

from ..database import SessionLocal
from ..models import Product, Sale
from ..services.printer import print_receipt


def _label(text, object_name=None):
    w = QLabel(text)
    if object_name:
        w.setObjectName(object_name)
    return w


def _money(value):
    return f"Rp {Decimal(str(value)):,.0f}".replace(",", ".")


def _search_products(window):
    dialog = QDialog(window)
    dialog.setWindowTitle("Cari Produk")
    dialog.resize(760, 480)
    root = QVBoxLayout(dialog)
    search = QLineEdit()
    search.setPlaceholderText("Nama produk atau barcode…")
    search.setText(window.barcode.text().strip())
    root.addWidget(search)
    table = QTableWidget(0, 4)
    table.setHorizontalHeaderLabels(["BARCODE", "PRODUK", "STOK", "HARGA"])
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    table.horizontalHeader().setStretchLastSection(True)
    root.addWidget(table, 1)

    def load_rows():
        text = search.text().strip()
        with SessionLocal() as session:
            query = session.query(Product).filter(Product.active.is_(True))
            if text:
                query = query.filter((Product.name.ilike(f"%{text}%")) | (Product.barcode.ilike(f"%{text}%")))
            products = query.order_by(Product.name).limit(100).all()
        table.setRowCount(len(products))
        for row, product in enumerate(products):
            for col, value in enumerate([product.barcode, product.name, str(product.stock), _money(product.selling_price)]):
                table.setItem(row, col, QTableWidgetItem(value))

    def choose():
        row = table.currentRow()
        if row < 0:
            QMessageBox.information(dialog, "Produk", "Pilih produk terlebih dahulu.")
            return
        window.barcode.setText(table.item(row, 0).text())
        dialog.accept()
        window.qty.setFocus()

    search.textChanged.connect(load_rows)
    table.cellDoubleClicked.connect(lambda row, _col: (table.selectRow(row), choose()))
    buttons = QDialogButtonBox(QDialogButtonBox.Cancel)
    select_button = QPushButton("Pilih Produk")
    buttons.addButton(select_button, QDialogButtonBox.AcceptRole)
    select_button.clicked.connect(choose)
    buttons.rejected.connect(dialog.reject)
    root.addWidget(buttons)
    load_rows()
    search.setFocus()
    dialog.exec()


def _selected_row(window):
    return window.cart_table.currentRow()


def _change_qty(window, delta):
    row = _selected_row(window)
    if row < 0 or row >= len(window.cart):
        return
    item = window.cart[row]
    new_qty = item["quantity"] + Decimal(str(delta))
    with SessionLocal() as session:
        product = session.get(Product, item["product_id"])
        if product is None:
            window.cart.pop(row)
        elif new_qty > Decimal(str(product.stock)):
            QMessageBox.warning(window, "Stok", f"Stok {product.name} tidak mencukupi.")
            return
        elif new_qty <= 0:
            window.cart.pop(row)
        else:
            item["quantity"] = new_qty
    window.refresh_cart()
    if window.cart:
        window.cart_table.selectRow(min(row, len(window.cart) - 1))


def _remove_item(window):
    row = _selected_row(window)
    if row < 0 or row >= len(window.cart):
        return
    name = window.cart_table.item(row, 1).text() if window.cart_table.item(row, 1) else "item"
    if QMessageBox.question(window, "Hapus Item", f"Hapus {name} dari keranjang?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
        return
    window.cart.pop(row)
    window.refresh_cart()


def _cancel(window):
    if not window.cart:
        window.clear_cart()
        return
    if QMessageBox.question(window, "Batal Transaksi", "Batalkan transaksi dan kosongkan keranjang?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
        window.clear_cart()


def _hold_current(window):
    if not window.cart:
        QMessageBox.information(window, "Parkir", "Keranjang masih kosong.")
        return
    name, ok = _text_input(window, "Parkir Transaksi", "Nama / label transaksi:")
    if not ok:
        return
    name = name.strip() or f"Parkir {len(window._held_sales) + 1}"
    window._held_sales.append({
        "label": name,
        "cart": [{"product_id": x["product_id"], "quantity": Decimal(str(x["quantity"]))} for x in window.cart],
        "discount": Decimal(str(window.discount.value())),
        "method": window.method.currentText(),
        "paid": Decimal(str(window.paid.value())),
    })
    window.clear_cart()
    QMessageBox.information(window, "Parkir", f"Transaksi '{name}' diparkir.")


def _text_input(parent, title, label):
    dialog = QDialog(parent)
    dialog.setWindowTitle(title)
    root = QVBoxLayout(dialog)
    root.addWidget(QLabel(label))
    edit = QLineEdit()
    edit.setPlaceholderText("Contoh: Pelanggan A / Meja 1")
    root.addWidget(edit)
    buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    root.addWidget(buttons)
    edit.setFocus()
    return (edit.text(), True) if dialog.exec() == QDialog.Accepted else ("", False)


def _show_held(window):
    dialog = QDialog(window)
    dialog.setWindowTitle("Transaksi Diparkir")
    dialog.resize(700, 420)
    root = QVBoxLayout(dialog)
    table = QTableWidget(0, 3)
    table.setHorizontalHeaderLabels(["LABEL", "ITEM", "TOTAL"])
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    table.horizontalHeader().setStretchLastSection(True)
    root.addWidget(table, 1)

    def reload_rows():
        table.setRowCount(len(window._held_sales))
        for row, held in enumerate(window._held_sales):
            total = Decimal("0")
            with SessionLocal() as session:
                for item in held["cart"]:
                    product = session.get(Product, item["product_id"])
                    if product:
                        total += Decimal(str(product.selling_price)) * item["quantity"]
            total = max(Decimal("0"), total - held["discount"])
            table.setItem(row, 0, QTableWidgetItem(held["label"]))
            table.setItem(row, 1, QTableWidgetItem(str(len(held["cart"]))))
            table.setItem(row, 2, QTableWidgetItem(_money(total)))

    reload_rows()
    actions = QHBoxLayout()
    resume = QPushButton("LANJUTKAN")
    delete = QPushButton("HAPUS PARKIR")
    close = QPushButton("TUTUP")
    actions.addWidget(resume)
    actions.addWidget(delete)
    actions.addStretch()
    actions.addWidget(close)
    root.addLayout(actions)

    def resume_selected():
        row = table.currentRow()
        if row < 0 or row >= len(window._held_sales):
            QMessageBox.information(dialog, "Parkir", "Pilih transaksi yang akan dilanjutkan.")
            return
        if window.cart and QMessageBox.question(window, "Keranjang Aktif", "Keranjang aktif akan diganti. Lanjutkan?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return
        held = window._held_sales.pop(row)
        window.cart = [{"product_id": x["product_id"], "quantity": Decimal(str(x["quantity"]))} for x in held["cart"]]
        window.discount.setValue(float(held["discount"]))
        window.method.setCurrentText(held["method"])
        window.paid.setValue(float(held["paid"]))
        window.refresh_cart()
        dialog.accept()
        window.barcode.setFocus()

    def delete_selected():
        row = table.currentRow()
        if row < 0 or row >= len(window._held_sales):
            return
        if QMessageBox.question(dialog, "Hapus Parkir", "Hapus transaksi yang diparkir?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No) != QMessageBox.Yes:
            return
        window._held_sales.pop(row)
        reload_rows()

    resume.clicked.connect(resume_selected)
    delete.clicked.connect(delete_selected)
    close.clicked.connect(dialog.accept)
    dialog.exec()


def _history(window):
    dialog = QDialog(window)
    dialog.setWindowTitle("Riwayat Transaksi")
    dialog.resize(900, 520)
    root = QVBoxLayout(dialog)
    table = QTableWidget(0, 5)
    table.setHorizontalHeaderLabels(["INVOICE", "WAKTU", "METODE", "TOTAL", "BAYAR"])
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    table.horizontalHeader().setStretchLastSection(True)
    root.addWidget(table, 1)
    with SessionLocal() as session:
        sales = session.query(Sale).order_by(Sale.created_at.desc()).limit(100).all()
        data = [(s.id, s.invoice_no, s.created_at, s.payment_method, s.total, s.paid) for s in sales]
    table.setRowCount(len(data))
    for row, item in enumerate(data):
        values = [item[1], item[2].strftime("%d/%m/%Y %H:%M:%S"), item[3], _money(item[4]), _money(item[5])]
        for col, value in enumerate(values):
            table.setItem(row, col, QTableWidgetItem(value))
    actions = QHBoxLayout()
    reprint = QPushButton("CETAK ULANG STRUK")
    close = QPushButton("TUTUP")
    actions.addWidget(reprint)
    actions.addStretch()
    actions.addWidget(close)
    root.addLayout(actions)

    def do_reprint():
        row = table.currentRow()
        if row < 0:
            QMessageBox.information(dialog, "Riwayat", "Pilih transaksi terlebih dahulu.")
            return
        try:
            with SessionLocal() as session:
                sale = session.get(Sale, data[row][0])
                if sale is None:
                    raise ValueError("Transaksi tidak ditemukan.")
                items = []
                for sale_item in sale.items:
                    product = session.get(Product, sale_item.product_id)
                    items.append({"name": product.name if product else "Produk", "quantity": sale_item.quantity, "unit_price": sale_item.unit_price, "line_total": sale_item.line_total})
                printed = print_receipt(window, sale, items)
            if printed:
                QMessageBox.information(dialog, "Cetak", f"Struk {sale.invoice_no} berhasil dicetak.")
            else:
                QMessageBox.warning(dialog, "Cetak", "Struk tidak dapat dicetak.")
        except Exception as exc:
            QMessageBox.critical(dialog, "Cetak gagal", str(exc))

    reprint.clicked.connect(do_reprint)
    close.clicked.connect(dialog.accept)
    dialog.exec()


def _install_shortcuts(window):
    shortcuts = []
    for key, callback in [("F4", window.checkout), ("Escape", lambda: _cancel(window)), ("F8", lambda: _history(window)), ("F9", lambda: _show_held(window)), ("F10", lambda: _hold_current(window))]:
        shortcut = QShortcut(QKeySequence(key), window)
        shortcut.activated.connect(callback)
        shortcuts.append(shortcut)
    window._cashier_shortcuts = shortcuts


def apply_premium_cashier(window):
    old_page = window.modern_stack.widget(1)
    current_index = window.modern_stack.currentIndex()
    window._held_sales = getattr(window, "_held_sales", [])

    page = QWidget()
    page.setObjectName("premiumCashierPage")
    root = QVBoxLayout(page)
    root.setContentsMargins(4, 4, 4, 4)
    root.setSpacing(10)

    scan = QFrame()
    scan.setObjectName("premiumScanCard")
    scan_l = QHBoxLayout(scan)
    scan_l.setContentsMargins(16, 12, 16, 12)
    scan_l.addWidget(_label("SCAN BARCODE", "premiumFieldCaption"))
    window.barcode = QLineEdit()
    window.barcode.setObjectName("premiumBarcode")
    window.barcode.setPlaceholderText("Scan barcode atau ketik kode produk…")
    window.barcode.returnPressed.connect(window.add_barcode)
    scan_l.addWidget(window.barcode, 1)
    scan_l.addWidget(_label("QTY", "premiumFieldCaption"))
    window.qty = QDoubleSpinBox()
    window.qty.setObjectName("premiumQty")
    window.qty.setRange(0.001, 999999)
    window.qty.setDecimals(3)
    window.qty.setValue(1)
    scan_l.addWidget(window.qty)
    add = QPushButton("+  TAMBAH")
    add.setObjectName("premiumAdd")
    add.clicked.connect(window.add_barcode)
    scan_l.addWidget(add)
    search = QPushButton("CARI PRODUK")
    search.setObjectName("premiumSearch")
    search.clicked.connect(lambda: _search_products(window))
    scan_l.addWidget(search)
    root.addWidget(scan)

    body = QHBoxLayout()
    body.setSpacing(12)
    cart_card = QFrame()
    cart_card.setObjectName("premiumCartCard")
    cart_l = QVBoxLayout(cart_card)
    cart_l.setContentsMargins(14, 12, 14, 14)
    head = QHBoxLayout()
    head.addWidget(_label("Keranjang Belanja", "premiumSectionTitle"))
    head.addStretch()
    head.addWidget(_label("PILIH BARIS UNTUK MENGUBAH QTY", "premiumMuted"))
    cart_l.addLayout(head)
    window.cart_table = QTableWidget(0, 5)
    window.cart_table.setObjectName("premiumCartTable")
    window.cart_table.setHorizontalHeaderLabels(["BARCODE", "PRODUK", "QTY", "HARGA", "SUBTOTAL"])
    window._prepare_table(window.cart_table)
    cart_l.addWidget(window.cart_table, 1)
    cart_actions = QHBoxLayout()
    for text, callback in [("− QTY", lambda: _change_qty(window, -1)), ("+ QTY", lambda: _change_qty(window, 1)), ("HAPUS ITEM", lambda: _remove_item(window))]:
        b = QPushButton(text); b.clicked.connect(callback); cart_actions.addWidget(b)
    cart_actions.addStretch()
    cart_l.addLayout(cart_actions)
    body.addWidget(cart_card, 1)

    pay_card = QFrame()
    pay_card.setObjectName("premiumPayCard")
    pay_card.setMinimumWidth(330)
    pay_l = QVBoxLayout(pay_card)
    pay_l.setContentsMargins(16, 14, 16, 14)
    pay_l.addWidget(_label("Ringkasan Pembayaran", "premiumSectionTitle"))
    total_box = QFrame(); total_box.setObjectName("premiumTotalBox"); total_l = QVBoxLayout(total_box)
    total_l.addWidget(_label("TOTAL TRANSAKSI", "premiumTotalCaption"))
    window.total_label = _label("Rp 0", "premiumTotal"); total_l.addWidget(window.total_label); pay_l.addWidget(total_box)
    discount_row = QHBoxLayout(); discount_row.addWidget(_label("Diskon", "premiumPayLabel"))
    window.discount = QDoubleSpinBox(); window.discount.setObjectName("premiumMoneyInput"); window.discount.setRange(0, 999999999); window.discount.setPrefix("Rp "); window.discount.valueChanged.connect(window.refresh_cart); discount_row.addWidget(window.discount, 1); pay_l.addLayout(discount_row)
    method_row = QHBoxLayout(); method_row.addWidget(_label("Metode", "premiumPayLabel"))
    window.method = QComboBox(); window.method.setObjectName("premiumMethod"); window.method.blockSignals(True); window.method.addItems(["CASH", "QRIS", "TRANSFER", "DEBIT"]); method_row.addWidget(window.method, 1); pay_l.addLayout(method_row)
    paid_row = QHBoxLayout(); paid_row.addWidget(_label("Bayar", "premiumPayLabel"))
    window.paid = QDoubleSpinBox(); window.paid.setObjectName("premiumMoneyInput"); window.paid.setRange(0, 999999999); window.paid.setPrefix("Rp "); paid_row.addWidget(window.paid, 1); pay_l.addLayout(paid_row)
    window.method.currentTextChanged.connect(window.payment_method_changed); window.method.blockSignals(False)
    change_box = QFrame(); change_box.setObjectName("premiumChangeBox"); change_l = QVBoxLayout(change_box)
    change_l.addWidget(_label("KEMBALIAN", "premiumChangeCaption")); window.change_label = _label("Rp 0", "premiumChange"); change_l.addWidget(window.change_label); pay_l.addWidget(change_box); pay_l.addStretch(1)

    actions = QHBoxLayout()
    for text, callback in [("PARKIR", lambda: _hold_current(window)), ("PARKIRAN", lambda: _show_held(window)), ("RIWAYAT", lambda: _history(window)), ("BATAL", lambda: _cancel(window)), ("CLEAR", lambda: _cancel(window))]:
        b = QPushButton(text); actions.addWidget(b); b.clicked.connect(callback)
    checkout = QPushButton("BAYAR & CETAK"); checkout.setObjectName("premiumCheckout"); checkout.clicked.connect(window.checkout); actions.addWidget(checkout, 1)
    pay_l.addLayout(actions)
    body.addWidget(pay_card, 0)
    root.addLayout(body, 1)

    window.modern_stack.removeWidget(old_page)
    window.modern_stack.insertWidget(1, page)
    old_page.deleteLater()
    if current_index == 1:
        window.modern_stack.setCurrentIndex(1)
    _install_shortcuts(window)
    window.barcode.setFocus()
