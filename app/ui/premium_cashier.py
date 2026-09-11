from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QDoubleSpinBox,
    QComboBox,
    QTableWidget,
    QWidget,
)


def _label(text, object_name=None):
    w = QLabel(text)
    if object_name:
        w.setObjectName(object_name)
    return w


def apply_premium_cashier(window):
    """Create the cashier page as a fresh live page in the modern stack.

    The previous implementation rebuilt the legacy page in place. In a
    QStackedWidget, that can preserve the old tab's hidden/visibility state
    and result in a completely blank Kasir page. The cashier business logic
    lives on MainWindow, so the page itself can safely be replaced.
    """
    old_page = window.modern_stack.widget(1)
    current_index = window.modern_stack.currentIndex()

    page = QWidget()
    page.setObjectName("premiumCashierPage")
    root = QVBoxLayout(page)
    root.setContentsMargins(4, 2, 4, 4)
    root.setSpacing(12)

    intro = QHBoxLayout()
    title_box = QVBoxLayout()
    title_box.setSpacing(2)
    title_box.addWidget(_label("Kasir", "premiumPageTitle"))
    title_box.addWidget(_label("Transaksi cepat · barcode first · offline", "premiumPageSubtitle"))
    intro.addLayout(title_box)
    intro.addStretch()
    intro.addWidget(
        _label("ENTER  Tambah  ·  F2  Fokus Barcode  ·  Ctrl+K  Cari", "premiumShortcut"),
        0,
        Qt.AlignBottom,
    )
    root.addLayout(intro)

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
    add.setToolTip("Tambah barang ke keranjang")
    add.clicked.connect(window.add_barcode)
    scan_l.addWidget(add)
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
    cart_head.addWidget(_label("ITEM AKAN MUNCUL DI SINI", "premiumMuted"))
    cart_l.addLayout(cart_head)
    window.cart_table = QTableWidget(0, 5)
    window.cart_table.setObjectName("premiumCartTable")
    window.cart_table.setHorizontalHeaderLabels(["BARCODE", "PRODUK", "QTY", "HARGA", "SUBTOTAL"])
    window._prepare_table(window.cart_table)
    cart_l.addWidget(window.cart_table, 1)
    body.addWidget(cart_card, 3)

    pay_card = QFrame()
    pay_card.setObjectName("premiumPayCard")
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
    clear.clicked.connect(window.clear_cart)
    buttons.addWidget(clear)
    checkout = QPushButton("BAYAR  &  CETAK")
    checkout.setObjectName("premiumCheckout")
    checkout.setMinimumHeight(48)
    checkout.setToolTip("Simpan transaksi dan cetak struk")
    checkout.clicked.connect(window.checkout)
    buttons.addWidget(checkout, 2)
    pay_l.addLayout(buttons)
    body.addWidget(pay_card, 1)
    root.addLayout(body, 1)

    window.modern_stack.removeWidget(old_page)
    window.modern_stack.insertWidget(1, page)
    old_page.deleteLater()
    if current_index == 1:
        window.modern_stack.setCurrentIndex(1)

    window.barcode.setFocus()
