from PySide6.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox, QHBoxLayout

from ..database import SessionLocal
from ..models import Product
from ..services.products import update_product


def _load_products_with_status(original, window):
    original(window)
    table = getattr(window, "product_table", None)
    if table is None:
        return
    if table.columnCount() < 9:
        table.setColumnCount(9)
        table.setHorizontalHeaderLabels([
            "ID", "Barcode", "Nama", "Kategori", "Satuan",
            "Beli", "Jual", "Stok", "Status"
        ])
    with SessionLocal() as session:
        rows = session.query(Product).order_by(Product.name).all()
        for row, product in enumerate(rows):
            if row >= table.rowCount():
                break
            table.setItem(row, 8, QTableWidgetItem("AKTIF" if product.active else "NONAKTIF"))


def _activate_selected(window):
    product_id = getattr(window, "selected_product_id", None)
    if not product_id:
        QMessageBox.warning(window, "Produk", "Pilih produk terlebih dahulu.")
        return
    try:
        with SessionLocal() as session:
            update_product(session, product_id, active=True)
        window.load_products()
        window.clear_product_form()
        QMessageBox.information(window, "Produk", "Produk berhasil diaktifkan.")
    except Exception as exc:
        QMessageBox.warning(window, "Produk", str(exc))


def apply_product_status_patch(MainWindow):
    original_load_products = MainWindow.load_products
    original_products = MainWindow.products

    def load_products(window):
        return _load_products_with_status(original_load_products, window)

    def products(window):
        widget = original_products(window)
        table = getattr(window, "product_table", None)
        if table is not None:
            if table.columnCount() < 9:
                table.setColumnCount(9)
                table.setHorizontalHeaderLabels([
                    "ID", "Barcode", "Nama", "Kategori", "Satuan",
                    "Beli", "Jual", "Stok", "Status"
                ])
            actions = QHBoxLayout()
            activate = QPushButton("Aktifkan")
            activate.setToolTip("Aktifkan kembali produk yang berstatus nonaktif")
            activate.clicked.connect(lambda: _activate_selected(window))
            actions.addWidget(activate)
            actions.addStretch()
            page_layout = widget.layout()
            if page_layout is not None:
                page_layout.insertLayout(3, actions)
        load_products(window)
        return widget

    MainWindow.load_products = load_products
    MainWindow.products = products
