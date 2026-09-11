from ..models import Product, SaleItem, PurchaseItem, StockMovement


def delete_product(session, product_id):
    """Permanently delete a product only when it has no historical references."""
    product = session.get(Product, product_id)
    if product is None:
        raise ValueError("Produk tidak ditemukan")

    if session.query(SaleItem).filter_by(product_id=product_id).first():
        raise ValueError("Produk tidak dapat dihapus karena sudah memiliki histori penjualan. Gunakan Nonaktifkan.")
    if session.query(PurchaseItem).filter_by(product_id=product_id).first():
        raise ValueError("Produk tidak dapat dihapus karena sudah memiliki histori pembelian. Gunakan Nonaktifkan.")
    if session.query(StockMovement).filter_by(product_id=product_id).first():
        raise ValueError("Produk tidak dapat dihapus karena sudah memiliki histori stok. Gunakan Nonaktifkan.")

    try:
        session.delete(product)
        session.commit()
    except Exception:
        session.rollback()
        raise

    return True
