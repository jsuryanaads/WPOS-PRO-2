from ..models import Product, StockMovement
from .validation import decimal_value


def adjust_stock(session, product_id, quantity, movement_type="ADJUSTMENT", reference=None):
    product = session.get(Product, product_id)
    try:
        qty = decimal_value(quantity, "Jumlah stok")
    except ValueError:
        raise
    if not product or qty == 0:
        raise ValueError("Produk/jumlah tidak valid")
    if product.stock + qty < 0:
        raise ValueError("Stok tidak boleh negatif")
    try:
        product.stock += qty
        session.add(StockMovement(product_id=product.id, movement_type=movement_type,
                                  quantity=qty, reference=reference))
        session.commit()
        return product
    except Exception:
        session.rollback()
        raise
