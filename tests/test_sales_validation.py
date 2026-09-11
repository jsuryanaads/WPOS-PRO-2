from decimal import Decimal
import pytest
from app.models import Product
from app.services.sales import create_sale
from tests.test_audit import make_session


def test_non_cash_requires_exact_payment():
    s = make_session()
    p = Product(barcode="N1", name="Barang", selling_price=10000, stock=2)
    s.add(p); s.commit()
    with pytest.raises(ValueError, match="non-tunai"):
        create_sale(s, [{"product_id": p.id, "quantity": 1}], 0, 9000, "QRIS", "INV-N1")
    assert s.get(Product, p.id).stock == Decimal("2.000")


def test_non_finite_values_are_rejected():
    s = make_session()
    p = Product(barcode="N2", name="Barang", selling_price=10000, stock=2)
    s.add(p); s.commit()
    with pytest.raises(ValueError, match="Pembayaran tidak valid"):
        create_sale(s, [{"product_id": p.id, "quantity": 1}], 0, "NaN", "CASH", "INV-N2")
