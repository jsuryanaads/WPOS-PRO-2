from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QDoubleSpinBox,
    QComboBox,
    QWidget,
)

from ..database import SessionLocal
from ..models import Product, Sale
from ..services.printer import print_receipt


def _label(text, object_name=None):
    w = QLabel(text)
    if object_name:
        w.setObjectName(object_name)
    return w


def _search_products(window):
    """Open a fast product lookup dialog using barcode/name search."""
    query = window.barcode.text().strip()
    dialog = QDialog(window)
    dialog.setWindowTitle("Cari Produk")
    dialog.resize(760, 480)
    root = QVBoxLayout(dialog)

    search = QLineEdit()
    search.setPlaceholderText("Ketik nama produk atau barcode…")
    search.setText(query)
    root.addWidget(search)

    table = QTableWidget(0, 4)
    table.setHorizontalHeaderLabels(["BARCODE", "PRODUK", "STOK", "HARGA"])
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setAlternatingRowColors(True)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(0, table.horizontalHeader().Stretch)
    table.horizontalHeader().setSectionResizeMode(1, table.horizontalHeader().Stretch)
    table.horizontalHeader().setSectionResizeMode(2, table.horizontalHeader().ResizeToContents)
    table.horizontalHeader().setSectionResizeMode(3, table.horizontalHeader().Stretch)
    root.addWidget(table, 1)

    def load_rows():
        text = search.text().strip()
        with SessionLocal() as session:
            q = session.query(Product).filter(Product.active.is_(True))
            if text:
                q = q.filter((Product.name.ilike(f"%{text}%")) | (Product.barcode.ilike(f"%{text}%")))
            rows = q.order_by(Product.name).limit(100).all()
        table.setRowCount(len(rows))
        for i, product in enumerate(rows):
            table.setItem(i, 0, QTableWidgetItem(product.barcode))
            table.setItem(i, 1, QTableWidgetItem(product.name))
            table.setItem(i, 2, QTableWidgetItem(str(product.stock)))
            table.setItem(i, 3, QTableWidgetItem(window._cashier_money(product.selling_price)))

    search.textChanged.connect(load_rows)

    buttons = QDialogButtonBox(QDialogButtonBox.Cancel)
    choose = QPushButton("Pilih Produk")
    buttons.addButton(choose, QDialogButtonBox.AcceptRole)
    root.addWidget(buttons)

    def choose_product():
        row = table.currentRow()
        if row < 0:
            QMessageBox.information(dialog, "Produk", "Pilih produk terlebih dahulu.")
            return
        window.barcode.setText(table.item(row, 0).text())
        dialog.accept()
        window.qty.setFocus()

    choose.clicked.connect(choose_product)
    table.cellDoubleClicked.connect(lambda row, _col: (table.selectRow(row), choose_product()))
    search.returnPressed.connect(lambda: (table.selectRow(0), choose_product()) if table.rowCount() else None)
    load_rows()
    search.setFocus()
    dialog.exec()


def _cart_row(window):
    return window.cart_table.currentRow()


def _change_cart_qty(window, delta):
    row = _cart_row(window)
    if row < 0 or row >= len(window.cart):
        return
    item = window.cart[row]
    with SessionLocal() as session:
        product = session.get(Product, item["product_id"])
        if product is None:
            window.cart.pop(row)
            window.refresh_cart()
            return
        new_qty = item["quantity"] + delta
        if new_qty > Decimal(str(product.stock)):
            QMessageBox.warning(window, "Stok", f"Stok {product.name} tidak mencukupi.")
            return
    if new_qty <= 0:
        window.cart.pop(row)
    else:
        item["quantity"] = new_qty
    window.refresh_cart()
    if window.cart:
        window.cart_table.selectRow(min(row, len(window.cart) - 1))


def _remove_cart_item(window):
    row = _cart_row(window)
    if row < 0 or row >= len(window.cart):
        return
    name = window.cart_table.item(row, 1).text() if window.cart_table.item(row, 1) else "item"
    answer = QMessageBox.question(
        window,
        "Hapus Item",
        f"Hapus {name} dari keranjang?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if answer != QMessageBox.Yes:
        return
    window.cart.pop(row)
    window.refresh_cart()


def _cancel_transaction(window):
    if not window.cart:
        window.clear_cart()
        return
    answer = QMessageBox.question(
        window,
        "Batal Transaksi",
        "Batalkan transaksi yang sedang berjalan dan kosongkan keranjang?",
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No,
    )
    if answer == QMessageBox.Yes:
        window.clear_cart()


def _show_history(window):
    """Show recent completed sales and allow receipt reprint."""
    dialog = QDialog(window)
    dialog.setWindowTitle("Riwayat Transaksi")
    dialog.resize(900, 520)
    root = QVBoxLayout(dialog)
    table = QTableWidget(0, 5)
    table.setHorizontalHeaderLabels(["INVOICE", "WAKTU", "METODE", "TOTAL", "BAYAR"])
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    table.setAlternatingRowColors(True)
    table.horizontalHeader().setStretchLastSection(True)
    root.addWidget(table, 1)

    with SessionLocal() as session:
        sales = session.query(Sale).order_by(Sale.created_at.desc()).limit(100).all()
        data = [
            (s.invoice_no, s.created_at.strftime("%d/%m/%Y %H:%M:%S"), s.payment_method, s.total, s.paid, s.id)
            for s in sales
        ]
    table.setRowCount(len(data))
    for i, row in enumerate(data):
        for c, value in enumerate(row[:5]):
            table.setItem(i, c, QTableWidgetItem(str(value) if c < 2 else window._cashier_money(value)))

    actions = QHBoxLayout()
    reprint = QPushButton("Cetak Ulang Struk")
    close = QPushButton("Tutup")
    actions.addWidget(reprint)
    actions.addStretch()
    actions.addWidget(close)
    root.addLayout(actions)

    def do_reprint():
        row = table.currentRow()
        if row < 0:
            QMessageBox.information(dialog, "Riwayat", "Pilih transaksi terlebih dahulu.")
            return
        sale_id = data[row][5]
        try:
            with SessionLocal() as session:
                sale = session.get(Sale, sale_id)
                if sale is None:
                    raise ValueError("Transaksi tidak ditemukan.")
                items = []
                for item in sale.items:
                    product = session.get(Product, item.product_id)
                    items.append({
                        "name": product.name if product else "Produk",
                        "quantity": item.quantity,
                        "unit_price": item.unit_price,
                        "line_total": item.line_total,
                    })
                printed = print_receipt(window, sale, items)
            if printed:
                QMessageBox.information(dialog, "Cetak", f"Struk {sale.invoice_no} berhasil dicetak.")
            else:
                QMessageBox.warning(dialog, "Cetak", "Printer tidak tersedia atau struk gagal dicetak.")
        except Exception as exc:
            QMessageBox.critical(dialog, "Cetak gagal", str(exc))

    reprint.clicked.connect(do_reprint)
    close.clicked.connect(dialog.accept)
    dialog.exec()


def _attach_cashier_features(window):
    """Attach cashier-only controls without changing sales service rules."""
    from decimal import Decimal

    window._cashier_money = lambda value: f"Rp {Decimal(str(value)):,.0f}".replace(",", ".")
    window._change_cart_qty = lambda delta: _change_cart_qty(window, Decimal(str(delta)))
    window._remove_cart_item = lambda: _remove_cart_item(window)
    window._cancel_transaction = lambda: _cancel_transaction(window)
    window._show_history = lambda: _show_history(window)

    search_button = QPushButton("CARI PRODUK")
    search_button.setObjectName("premiumSearch")
    search_button.setToolTip("Cari berdasarkan nama atau barcode")
    search_button.clicked.connect(lambda: _search_products(window))
    window._cashier_search_button = search_button

    # Keep the existing cart table columns/business refresh intact and add a
    # separate action bar so no transaction model or create_sale contract changes.
    actions = QHBoxLayout()
    minus = QPushButton("−  QTY")
    plus = QPushButton("+  QTY")
    remove = QPushButton("HAPUS ITEM")
    cancel = QPushButton("BATAL TRANSAKSI")
    history = QPushButton("RIWAYAT")
    minus.setToolTip("Kurangi 1 dari item terpilih")
    plus.setToolTip("Tambah 1 ke item terpilih")
    remove.setToolTip("Hapus item terpilih dari keranjang")
    cancel.setToolTip("Batalkan transaksi yang sedang berjalan")
    history.setToolTip("Lihat transaksi tersimpan dan cetak ulang struk")
    minus.clicked.connect(lambda: _change_cart_qty(window, Decimal("-1")))
    plus.clicked.connect(lambda: _change_cart_qty(window, Decimal("1")))
    remove.clicked.connect(lambda: _remove_cart_item(window))
    cancel.clicked.connect(lambda: _cancel_transaction(window))
    history.clicked.connect(lambda: _show_history(window))
    actions.addWidget(minus)
    actions.addWidget(plus)
    actions.addWidget(remove)
    actions.addStretch()
    actions.addWidget(history)
    actions.addWidget(cancel)
    window._cashier_actions = actions

    # Keyboard workflow for a one-computer counter.
    QShortcut(QKeySequence("F4"), window, activated=window.checkout)
    QShortcut(QKeySequence("Escape"), window, activated=lambda: _cancel_transaction(window))
    QShortcut(QKeySequence("F8"), window, activated=lambda: _show_history(window))


def apply_premium_cashier(window):
    """Build the modern cashier workflow while preserving MainWindow services."""
    from decimal import Decimal

    old_page = window.modern_stack.widget(1)
    current_index = window.modern_stack.currentIndex()

    page = QWidget()
    page.setObjectName("premiumCashierPage")
    root = QVBoxLayout(page)
    root.setContentsMargins(4, 4, 4, 4)
    root.setSpacing(10)

    scan = QFrame()
    scan.setObjectName("premiumScanCard")
    scan_l = QHBoxLayout(scan)
    scan_l.setContentsMargins(16, 12, 16, 12)
    scan_l.setSpacing(10)
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
    search_button = QPushButton("CARI")
    search_button.setObjectName("premiumSearch")
    scan_l.addWidget(search_button)
    root.addWidget(scan)

    body = QHBoxLayout()
    body.setSpacing(12)

    cart_card = QFrame()
    cart_card.setObjectName("premiumCartCard")
    cart_l = QVBoxLayout(cart_card)
    cart_l.setContentsMargins(14, 12, 14, 14)
    cart_l.setSpacing(8)
    cart_head = QHBoxLayout()
    cart_head.addWidget(_label("Keranjang Belanja", "premiumSectionTitle"))
    cart_head.addStretch()
    cart_head.addWidget(_label("PILIH BARIS UNTUK QTY / HAPUS", "premiumMuted"))
    cart_l.addLayout(cart_head)
    window.cart_table = QTableWidget(0, 5)
    window.cart_table.setObjectName("premiumCartTable")
    window.cart_table.setHorizontalHeaderLabels(["BARCODE", "PRODUK", "QTY", "HARGA", "SUBTOTAL"])
    window._prepare_table(window.cart_table)
    cart_l.addWidget(window.cart_table, 1)
    cart_actions = QHBoxLayout()
    cart_actions.addWidget(QPushButton("− QTY", clicked=lambda: _change_cart_qty(window, Decimal("-1"))))
    cart_actions.addWidget(QPushButton("+ QTY", clicked=lambda: _change_cart_qty(window, Decimal("1"))))
    cart_actions.addWidget(QPushButton("HAPUS ITEM", clicked=lambda: _remove_cart_item(window)))
    cart_actions.addStretch()
    cart_l.addLayout(cart_actions)
    body.addWidget(cart_card, 1)

    pay_card = QFrame()
    pay_card.setObjectName("premiumPayCard")
    pay_card.setMinimumWidth(330)
    pay_l = QVBoxLayout(pay_card)
    pay_l.setContentsMargins(16, 14, 16, 14)
    pay_l.setSpacing(10)
    pay_l.addWidget(_label("Ringkasan Pembayaran", "premiumSectionTitle"))

    total_box = QFrame()
    total_box.setObjectName("premiumTotalBox")
    total_l = QVBoxLayout(total_box)
    total_l.setContentsMargins(14, 12, 14, 12)
    total_l.addWidget(_label("TOTAL TRANSAKSI", "premiumTotalCaption"))
    window.total_label = _label("Rp 0", "premiumTotal")
    total_l.addWidget(window.total_label)
    pay_l.addWidget(total_box)

    discount_row = QHBoxLayout()
    discount_row.addWidget(_label("Diskon", "premiumPayLabel"))
    window.discount = QDoubleSpinBox()
    window.discount.setObjectName("premiumMoneyInput")
    window.discount.setRange(0, 999999999)
    window.discount.setPrefix("Rp ")
    window.discount.valueChanged.connect(window.refresh_cart)
    discount_row.addWidget(window.discount, 1)
    pay_l.addLayout(discount_row)

    method_row = QHBoxLayout()
    method_row.addWidget(_label("Metode", "premiumPayLabel"))
    window.method = QComboBox()
    window.method.setObjectName("premiumMethod")
    window.method.blockSignals(True)
    window.method.addItems(["CASH", "QRIS", "TRANSFER", "DEBIT"])
    method_row.addWidget(window.method, 1)
    pay_l.addLayout(method_row)

    paid_row = QHBoxLayout()
    paid_row.addWidget(_label("Bayar", "premiumPayLabel"))
    window.paid = QDoubleSpinBox()
    window.paid.setObjectName("premiumMoneyInput")
    window.paid.setRange(0, 999999999)
    window.paid.setPrefix("Rp ")
    paid_row.addWidget(window.paid, 1)
    pay_l.addLayout(paid_row)

    window.method.currentTextChanged.connect(window.payment_method_changed)
    window.method.blockSignals(False)

    change_box = QFrame()
    change_box.setObjectName("premiumChangeBox")
    change_l = QVBoxLayout(change_box)
    change_l.setContentsMargins(12, 9, 12, 9)
    change_l.addWidget(_label("KEMBALIAN", "premiumChangeCaption"))
    window.change_label = _label("Rp 0", "premiumChange")
    change_l.addWidget(window.change_label)
    pay_l.addWidget(change_box)
    pay_l.addStretch(1)

    buttons = QHBoxLayout()
    clear = QPushButton("CLEAR")
    clear.setObjectName("premiumClear")
    clear.setMinimumHeight(48)
    clear.clicked.connect(lambda: _cancel_transaction(window))
    buttons.addWidget(clear)
    checkout = QPushButton("BAYAR & CETAK")
    checkout.setObjectName("premiumCheckout")
    checkout.setMinimumHeight(48)
    checkout.setMinimumWidth(165)
    checkout.clicked.connect(window.checkout)
    buttons.addWidget(checkout, 1)
    pay_l.addLayout(buttons)
    body.addWidget(pay_card, 0)
    root.addLayout(body, 1)

    window.modern_stack.removeWidget(old_page)
    window.modern_stack.insertWidget(1, page)
    old_page.deleteLater()
    if current_index == 1:
        window.modern_stack.setCurrentIndex(1)

    search_button.clicked.connect(lambda: _search_products(window))
    _attach_cashier_features(window)
    window.barcode.setFocus()
