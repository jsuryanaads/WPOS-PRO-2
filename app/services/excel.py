from decimal import Decimal
from pathlib import Path

from openpyxl import Workbook, load_workbook

from ..models import Category, Product, Unit, StockMovement
from .validation import decimal_value

PRODUCT_HEADERS = [
    "Barcode", "Nama Produk", "Kategori", "Satuan",
    "Harga Beli", "Harga Jual", "Stok Awal", "Stok Minimum", "Aktif",
]


def export_products(session, path):
    path = Path(path)
    if path.suffix.lower() != ".xlsx":
        path = path.with_suffix(".xlsx")
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Produk"
    sheet.append(PRODUCT_HEADERS)
    categories = {row.id: row.name for row in session.query(Category).all()}
    units = {row.id: row.name for row in session.query(Unit).all()}
    products = session.query(Product).order_by(Product.name).all()
    for product in products:
        sheet.append([
            product.barcode, product.name,
            categories.get(product.category_id, ""), units.get(product.unit_id, ""),
            float(product.purchase_price), float(product.selling_price),
            float(product.stock), float(product.minimum_stock),
            "YA" if product.active else "TIDAK",
        ])
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    for column in sheet.columns:
        width = min(max(len(str(cell.value or "")) for cell in column) + 2, 40)
        sheet.column_dimensions[column[0].column_letter].width = width
    workbook.save(path)
    return path


def _text(value):
    return "" if value is None else str(value).strip()


def _number(value, label, default="0"):
    value = default if value is None or _text(value) == "" else value
    return decimal_value(value, label, non_negative=True)


def _lookup(session, model, name, label):
    name = _text(name)
    if not name:
        return None
    row = session.query(model).filter(model.name == name).first()
    if row is None:
        raise ValueError(f"{label} tidak ditemukan: {name}")
    return row.id


def _active(value):
    text = _text(value).upper()
    if text in ("", "YA", "YES", "TRUE", "1", "AKTIF"):
        return True
    if text in ("TIDAK", "NO", "FALSE", "0", "NONAKTIF"):
        return False
    raise ValueError("Kolom Aktif harus YA atau TIDAK")


def import_products(session, path, mode="add"):
    if mode not in ("add", "update"):
        raise ValueError("Mode import tidak valid")
    workbook = load_workbook(Path(path), read_only=True, data_only=True)
    try:
        rows = list(workbook.active.iter_rows(values_only=True))
    finally:
        workbook.close()
    if not rows:
        raise ValueError("File Excel kosong")
    if [_text(value) for value in rows[0]] != PRODUCT_HEADERS:
        raise ValueError("Format Excel tidak sesuai. Gunakan file hasil Export Produk sebagai template.")

    prepared, errors, seen = [], [], set()
    for row_number, values in enumerate(rows[1:], start=2):
        if not any(value is not None and _text(value) for value in values):
            continue
        try:
            data = dict(zip(PRODUCT_HEADERS, values))
            barcode, name = _text(data["Barcode"]), _text(data["Nama Produk"])
            if not barcode or not name:
                raise ValueError("Barcode dan Nama Produk wajib diisi")
            if barcode in seen:
                raise ValueError("Barcode duplikat di dalam file")
            seen.add(barcode)
            prepared.append({
                "barcode": barcode, "name": name,
                "category_id": _lookup(session, Category, data["Kategori"], "Kategori"),
                "unit_id": _lookup(session, Unit, data["Satuan"], "Satuan"),
                "purchase_price": _number(data["Harga Beli"], "Harga beli"),
                "selling_price": _number(data["Harga Jual"], "Harga jual"),
                "stock": _number(data["Stok Awal"], "Stok awal"),
                "minimum_stock": _number(data["Stok Minimum"], "Stok minimum"),
                "active": _active(data["Aktif"]),
            })
        except Exception as exc:
            errors.append(f"Baris {row_number}: {exc}")
    if errors:
        raise ValueError("Import dibatalkan:\n" + "\n".join(errors[:20]))

    created = updated = 0
    try:
        for data in prepared:
            existing = session.query(Product).filter_by(barcode=data["barcode"]).first()
            if existing:
                if mode != "update":
                    raise ValueError(f"Barcode sudah digunakan: {data['barcode']}")
                existing.name = data["name"]
                existing.category_id = data["category_id"]
                existing.unit_id = data["unit_id"]
                existing.purchase_price = data["purchase_price"]
                existing.selling_price = data["selling_price"]
                existing.minimum_stock = data["minimum_stock"]
                existing.active = data["active"]
                # Stok berjalan tidak diubah oleh import Excel.
                updated += 1
            else:
                product = Product(
                    barcode=data["barcode"], name=data["name"],
                    category_id=data["category_id"], unit_id=data["unit_id"],
                    purchase_price=data["purchase_price"], selling_price=data["selling_price"],
                    stock=data["stock"], minimum_stock=data["minimum_stock"], active=data["active"],
                )
                session.add(product)
                session.flush()
                if data["stock"] > 0:
                    session.add(StockMovement(
                        product_id=product.id, movement_type="OPENING",
                        quantity=data["stock"], reference="IMPORT-EXCEL",
                    ))
                created += 1
        session.commit()
        return {"created": created, "updated": updated}
    except Exception:
        session.rollback()
        raise
