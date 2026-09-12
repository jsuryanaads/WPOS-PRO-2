"""Multi-item purchase presentation for WPOS PRO 2.

Business rules remain in services.purchases.create_purchase. This module only
owns the purchase-entry UI state and delegates persistence to that service.
"""

from datetime import datetime
from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..database import SessionLocal
from ..models import Product, Supplier
from ..services.purchases import create_purchase


def _money(value):
    return f"Rp {Decimal(str(value)):,.0f}".replace(",", ".")


def purchase_page(window):
    """Build a purchase page that supports multiple products per invoice."""
    w = QWidget()
    w.setObjectName("purchasePage")
    layout = QVBoxLayout(w)
    layout.setContentsMargins(18, 16, 18, 18)
    layout.setSpacing(10)

    header = window.page_header(
        "Pembelian",
        "Susun banyak produk dalam satu invoice supplier, lalu tambah stok sekaligus.",
    )
    layout.addWidget(header)

    meta = QGroupBox("Informasi Pembelian")
    form = QFormLayout(meta)
    window.buy_supplier = QComboBox()
    window.buy_invoice = QLineEdit()
    window.buy_invoice.setPlaceholderText("Kosongkan untuk nomor otomatis")
    form.addRow("Supplier", window.buy_supplier)
    form.addRow("No. Invoice", window.buy_invoice)
    layout.addWidget(meta)

    entry = QGroupBox("Tambah Item")
    entry_row = QHBoxLayout(entry)
    window.buy_product = QComboBox()
    window.buy_qty = QDoubleSpinBox()
    window.buy_qty.setRange(0.001, 999999)
    window.buy_qty.setDecimals(3)
    window.buy_qty.setValue(1)
    window.buy_cost = QDoubleSpinBox()
    window.buy_cost.setRange(0, 999999999)
    window.buy_cost.setDecimals(0)
    add = QPushButton("Tambah Item")
    add.setObjectName("primary")
    add.clicked.connect(window.add_purchase_item)
    entry_row.addWidget(QLabel("Produk"))
    entry_row.addWidget(window.buy_product, 3)
    entry_row.addWidget(QLabel("Qty"))
    entry_row.addWidget(window.buy_qty)
    entry_row.addWidget(QLabel("Harga Beli"))
    entry_row.addWidget(window.buy_cost)
    entry_row.addWidget(add)
    layout.addWidget(entry)

    window.purchase_table = QTableWidget(0, 6)
    window.purchase_table.setObjectName("purchaseItemsTable")
    window.purchase_table.setHorizontalHeaderLabels(
        ["Produk", "Barcode", "Qty", "Harga Beli", "Subtotal", "Aksi"]
    )
    window.purchase_table.setSelectionBehavior(QTableWidget.SelectRows)
    window.purchase_table.setEditTriggers(QTableWidget.NoEditTriggers)
    window.purchase_table.horizontalHeader().setStretchLastSection(False)
    window.purchase_table.horizontalHeader().setSectionResizeMode(0, window.purchase_table.horizontalHeader().Stretch)
    for col in (1, 2, 3, 4, 5):
        window.purchase_table.horizontalHeader().setSectionResizeMode(col, window.purchase_table.horizontalHeader().ResizeToContents)
    layout.addWidget(window.purchase_table, 1)

    summary = QFrame()
    summary.setObjectName("purchaseSummary")
    summary_row = QHBoxLayout(summary)
    summary_row.setContentsMargins(12, 8, 12, 8)
    window.purchase_count_label = QLabel("0 item")
    window.purchase_total_label = QLabel("TOTAL PEMBELIAN Rp 0")
    window.purchase_total_label.setObjectName("total")
    summary_row.addWidget(window.purchase_count_label)
    summary_row.addStretch()
    summary_row.addWidget(window.purchase_total_label)
    layout.addWidget(summary)

    actions = QHBoxLayout()
    clear = QPushButton("CLEAR ITEM")
    clear.clicked.connect(window.clear_purchase_items)
    save = QPushButton("SIMPAN PEMBELIAN & TAMBAH STOK")
    save.setObjectName("primary")
    save.clicked.connect(window.save_purchase)
    actions.addWidget(clear)
    actions.addStretch()
    actions.addWidget(save)
    layout.addLayout(actions)

    window.purchase_items = []
    window.load_purchase_options()
    return w


def install_purchase_methods(window):
    """Install purchase-page methods on a MainWindow-compatible instance."""
    # Kept as a small compatibility hook for future UI shells.
    return window


def load_purchase_options(window):
    with SessionLocal() as session:
        products = session.query(Product).filter_by(active=True).order_by(Product.name).all()
        suppliers = session.query(Supplier).order_by(Supplier.name).all()
    window.buy_product.clear()
    window.buy_supplier.clear()
    for product in products:
        window.buy_product.addItem(f"{product.name} | {product.barcode}", product.id)
    window.buy_supplier.addItem("Tanpa Supplier", None)
    for supplier in suppliers:
        window.buy_supplier.addItem(supplier.name, supplier.id)


def add_purchase_item(window):
    product_id = window.buy_product.currentData()
    if product_id is None:
        QMessageBox.warning(window, "Pembelian", "Belum ada produk aktif.")
        return
    qty = Decimal(str(window.buy_qty.value()))
    cost = Decimal(str(window.buy_cost.value()))
    if qty <= 0:
        QMessageBox.warning(window, "Pembelian", "Qty harus lebih besar dari 0.")
        return
    if cost < 0:
        QMessageBox.warning(window, "Pembelian", "Harga beli tidak boleh negatif.")
        return

    with SessionLocal() as session:
        product = session.get(Product, int(product_id))
        if not product or not product.active:
            QMessageBox.warning(window, "Pembelian", "Produk tidak ditemukan atau tidak aktif.")
            return
        name = product.name
        barcode = product.barcode

    existing = next((row for row in window.purchase_items if row["product_id"] == int(product_id)), None)
    if existing:
        existing["quantity"] += qty
        existing["unit_cost"] = cost
    else:
        window.purchase_items.append(
            {"product_id": int(product_id), "name": name, "barcode": barcode, "quantity": qty, "unit_cost": cost}
        )
    window.buy_qty.setValue(1)
    window.buy_cost.setValue(0)
    refresh_purchase_table(window)
    window.buy_product.setFocus()


def remove_purchase_item(window, row_index):
    if 0 <= row_index < len(window.purchase_items):
        window.purchase_items.pop(row_index)
        refresh_purchase_table(window)


def refresh_purchase_table(window):
    rows = window.purchase_items
    window.purchase_table.setRowCount(len(rows))
    total = Decimal("0")
    for row_index, row in enumerate(rows):
        subtotal = row["quantity"] * row["unit_cost"]
        total += subtotal
        values = [
            row["name"],
            row["barcode"],
            str(row["quantity"]),
            _money(row["unit_cost"]),
            _money(subtotal),
        ]
        for col, value in enumerate(values):
            window.purchase_table.setItem(row_index, col, QTableWidgetItem(str(value)))
        remove = QPushButton("Hapus")
        remove.clicked.connect(lambda _checked=False, idx=row_index: remove_purchase_item(window, idx))
        window.purchase_table.setCellWidget(row_index, 5, remove)
    window.purchase_count_label.setText(f"{len(rows)} item")
    window.purchase_total_label.setText(f"TOTAL PEMBELIAN {_money(total)}")
    return total


def clear_purchase_items(window):
    window.purchase_items.clear()
    refresh_purchase_table(window)


def save_purchase(window):
    try:
        if not window.purchase_items:
            raise ValueError("Item pembelian kosong")
        invoice = window.buy_invoice.text().strip() or "PB-" + datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        items = [
            {
                "product_id": row["product_id"],
                "quantity": row["quantity"],
                "unit_cost": row["unit_cost"],
            }
            for row in window.purchase_items
        ]
        with SessionLocal() as session:
            create_purchase(session, items, window.buy_supplier.currentData(), invoice)
        QMessageBox.information(
            window,
            "Pembelian",
            f"Pembelian {invoice} tersimpan.\n{len(items)} item ditambahkan dan stok bertambah.",
        )
        clear_purchase_items(window)
        window.buy_invoice.clear()
        window.buy_qty.setValue(1)
        window.buy_cost.setValue(0)
        window.load_purchase_options()
        if hasattr(window, "load_stock_table"):
            window.load_stock_table()
        if hasattr(window, "load_stock_products"):
            window.load_stock_products()
        if hasattr(window, "load_products"):
            window.load_products()
    except Exception as exc:
        QMessageBox.warning(window, "Pembelian", str(exc))
