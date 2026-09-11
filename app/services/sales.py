from decimal import Decimal, InvalidOperation
from ..models import Sale, SaleItem, Product, StockMovement, CashMovement

PAYMENT_METHODS = {"CASH", "QRIS", "TRANSFER", "DEBIT"}


def _decimal(value, label):
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(f"{label} tidak valid")
    if not result.is_finite():
        raise ValueError(f"{label} tidak valid")
    return result


def create_sale(session, items, discount, paid, payment_method, invoice_no):
    if not items:
        raise ValueError("Keranjang kosong")
    discount = _decimal(discount, "Diskon")
    paid = _decimal(paid, "Pembayaran")
    payment_method = str(payment_method).upper().strip()
    invoice_no = str(invoice_no).strip()
    if not invoice_no:
        raise ValueError("Nomor invoice wajib diisi")
    if discount < 0 or paid < 0:
        raise ValueError("Diskon/pembayaran tidak valid")
    if payment_method not in PAYMENT_METHODS:
        raise ValueError("Metode pembayaran tidak valid")
    if session.query(Sale).filter_by(invoice_no=invoice_no).first():
        raise ValueError("Nomor invoice sudah digunakan")

    products = {}
    requested = {}
    normalized_items = []
    try:
        for row in items:
            product_id = int(row["product_id"])
            qty = _decimal(row["quantity"], "Jumlah")
            if qty <= 0:
                raise ValueError("Jumlah tidak valid")
            product = session.get(Product, product_id)
            if not product or not product.active:
                raise ValueError("Produk tidak ditemukan/tidak aktif")
            products[product.id] = product
            requested[product.id] = requested.get(product.id, Decimal("0")) + qty
            normalized_items.append((product, qty))

        for product_id, qty in requested.items():
            if Decimal(str(products[product_id].stock)) < qty:
                raise ValueError(f"Stok {products[product_id].name} tidak mencukupi")

        subtotal = sum((Decimal(str(product.selling_price)) * qty for product, qty in normalized_items), Decimal("0"))
        if discount > subtotal:
            discount = subtotal
        total = subtotal - discount

        if payment_method == "CASH":
            if paid < total:
                raise ValueError("Pembayaran kurang")
            change = paid - total
        else:
            if paid != total:
                raise ValueError("Pembayaran non-tunai harus sama dengan total")
            change = Decimal("0")

        sale = Sale(invoice_no=invoice_no, subtotal=subtotal, discount=discount,
                    total=total, paid=paid, change=change, payment_method=payment_method)
        session.add(sale)
        session.flush()
        for product, qty in normalized_items:
            line = Decimal(str(product.selling_price)) * qty
            sale.items.append(SaleItem(product_id=product.id, quantity=qty,
                                       unit_price=product.selling_price, line_total=line))
            product.stock -= qty
            session.add(StockMovement(product_id=product.id, movement_type="SALE",
                                      quantity=-qty, reference=invoice_no))
        if payment_method == "CASH":
            session.add(CashMovement(movement_type="SALE", amount=total, reference=invoice_no))
        session.commit()
        return sale
    except Exception:
        session.rollback()
        raise
