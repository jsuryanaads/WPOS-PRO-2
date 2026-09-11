from decimal import Decimal, InvalidOperation
from ..models import Product, StockMovement


def _decimal(value, label):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValueError(f"{label} tidak valid")
    if result < 0:
        raise ValueError(f"{label} tidak boleh negatif")
    return result


def create_product(session, barcode, name, purchase_price=0, selling_price=0, stock=0, minimum_stock=0, category_id=None, unit_id=None):
    barcode = str(barcode).strip()
    name = str(name).strip()
    if not barcode or not name:
        raise ValueError("Barcode dan nama wajib diisi")
    if session.query(Product).filter_by(barcode=barcode).first():
        raise ValueError("Barcode sudah digunakan")
    opening_stock = _decimal(stock, "Stok")
    product = Product(
        barcode=barcode, name=name,
        purchase_price=_decimal(purchase_price, "Harga beli"),
        selling_price=_decimal(selling_price, "Harga jual"),
        stock=opening_stock,
        minimum_stock=_decimal(minimum_stock, "Stok minimum"),
        category_id=category_id, unit_id=unit_id,
    )
    try:
        session.add(product)
        session.flush()
        if opening_stock > 0:
            session.add(StockMovement(
                product_id=product.id,
                movement_type="OPENING",
                quantity=opening_stock,
                reference="STOK-AWAL",
            ))
        session.commit()
        session.refresh(product)
        return product
    except Exception:
        session.rollback()
        raise


def update_product(session, product_id, **changes):
    product = session.get(Product, product_id)
    if not product:
        raise ValueError("Produk tidak ditemukan")
    if "barcode" in changes:
        barcode = str(changes["barcode"]).strip()
        if not barcode:
            raise ValueError("Barcode wajib diisi")
        duplicate = session.query(Product).filter(Product.barcode == barcode, Product.id != product.id).first()
        if duplicate:
            raise ValueError("Barcode sudah digunakan")
        product.barcode = barcode
    if "name" in changes:
        name = str(changes["name"]).strip()
        if not name:
            raise ValueError("Nama wajib diisi")
        product.name = name
    for field, label in (("purchase_price", "Harga beli"), ("selling_price", "Harga jual"), ("minimum_stock", "Stok minimum")):
        if field in changes:
            setattr(product, field, _decimal(changes[field], label))
    for field in ("category_id", "unit_id", "active"):
        if field in changes:
            setattr(product, field, changes[field])
    try:
        session.commit()
        session.refresh(product)
        return product
    except Exception:
        session.rollback()
        raise


def deactivate_product(session, product_id):
    return update_product(session, product_id, active=False)
