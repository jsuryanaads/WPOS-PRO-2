from PySide6.QtWidgets import QTableWidgetItem, QPushButton, QMessageBox

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
            status = "AKTIF" if product.active else "NONAKTIF"
            table.setItem(row, 8, QTableWidgetItem(status))


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
            activate = QPushButton("Aktifkan")
            activate.setToolTip("Aktifkan kembali produk yang berstatus nonaktif")
            activate.clicked.connect(lambda: _activate_selected(window))
            # Insert the action next to the existing product controls.
            controls = table.parentWidget()
            while controls is not None and not hasattr(controls, "layout"):
                controls = controls.parentWidget()
            if controls is not None:
                layout = controls.layout()
                if layout is not None:
                    for i in range(layout.count()):
                        item = layout.itemAt(i)
                        child = item.widget() if item else None
                        if child is not None and child.text() == "Nonaktifkan":
                            layout.insertWidget(i + 1, activate)
                            break
        load_products(window)
        return widget

    MainWindow.load_products = load_products
    MainWindow.products = products
