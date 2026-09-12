"""Presentation helpers for the Produk table.

This module changes only how product stock/status are rendered in the UI.
Database values and product business rules remain untouched.
"""

from decimal import Decimal

from PySide6.QtWidgets import QTableWidgetItem

from ..database import SessionLocal
from ..models import Product


def _whole_number(value):
    try:
        number = Decimal(str(value))
    except Exception:
        return str(value)
    if number == number.to_integral_value():
        return str(number.quantize(Decimal("1")))
    return format(number.normalize(), "f")


def apply_product_table_display(window):
    """Normalize Product stock display and add an explicit Active status column."""
    table = getattr(window, "product_table", None)
    if table is None:
        return

    headers = [
        table.horizontalHeaderItem(i).text() if table.horizontalHeaderItem(i) else ""
        for i in range(table.columnCount())
    ]
    if "Status" not in headers:
        table.setColumnCount(table.columnCount() + 1)
        table.setHorizontalHeaderLabels(headers + ["Status"])
        headers.append("Status")

    stock_col = headers.index("Stok") if "Stok" in headers else -1
    id_col = headers.index("ID") if "ID" in headers else -1
    status_col = headers.index("Status")

    ids = []
    for row in range(table.rowCount()):
        cell = table.item(row, id_col) if id_col >= 0 else None
        try:
            ids.append(int(cell.text()))
        except (AttributeError, TypeError, ValueError):
            ids.append(None)
        if stock_col >= 0:
            stock_item = table.item(row, stock_col)
            if stock_item is not None:
                stock_item.setText(_whole_number(stock_item.text()))

    active_by_id = {}
    valid_ids = [value for value in ids if value is not None]
    if valid_ids:
        with SessionLocal() as session:
            rows = session.query(Product.id, Product.active).filter(Product.id.in_(valid_ids)).all()
            active_by_id = {product_id: bool(active) for product_id, active in rows}

    for row, product_id in enumerate(ids):
        status = "AKTIF" if active_by_id.get(product_id, False) else "NONAKTIF"
        table.setItem(row, status_col, QTableWidgetItem(status))

    table.resizeColumnsToContents()
