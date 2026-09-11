from decimal import Decimal
from ..models import Purchase, PurchaseItem, Product, Supplier, StockMovement


def create_purchase(session, items, supplier_id, invoice_no):
    if not items:
        raise ValueError("Item pembelian kosong")
    invoice_no = str(invoice_no).strip()
    if not invoice_no:
        raise ValueError("Nomor pembelian wajib diisi")
    if session.query(Purchase).filter_by(invoice_no=invoice_no).first():
        raise ValueError("Nomor pembelian sudah digunakan")

    supplier = None
    if supplier_id is not None:
        supplier = session.get(Supplier, int(supplier_id))
        if not supplier:
            raise ValueError("Supplier tidak ditemukan")

    total = Decimal("0")
    normalized_items = []
    try:
        for row in items:
            product_id = int(row["product_id"])
            qty = Decimal(str(row["quantity"]))
            cost = Decimal(str(row["unit_cost"]))
            if qty <= 0 or cost < 0:
                raise ValueError("Jumlah/harga pembelian tidak valid")
            product = session.get(Product, product_id)
            if not product or not product.active:
                raise ValueError("Produk tidak ditemukan/tidak aktif")
            normalized_items.append((product, qty, cost))
            total += qty * cost

        purchase = Purchase(invoice_no=invoice_no, supplier_id=supplier.id if supplier else None, total=total)
        session.add(purchase)
        session.flush()
        for product, qty, cost in normalized_items:
            purchase.items.append(PurchaseItem(product_id=product.id, quantity=qty,
                                               unit_cost=cost, line_total=qty * cost))
            product.stock += qty
            product.purchase_price = cost
            session.add(StockMovement(product_id=product.id, movement_type="PURCHASE",
                                      quantity=qty, reference=invoice_no))
        session.commit()
        return purchase
    except Exception:
        session.rollback()
        raise
