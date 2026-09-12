from datetime import datetime
from decimal import Decimal

from app.services import printer


class _User:
    def __init__(self, name):
        self.name = name


def _sale():
    return type("SaleStub", (), {
        "invoice_no": "INV-TEST-001",
        "created_at": datetime(2026, 9, 12, 16, 30, 0),
        "subtotal": Decimal("12000"),
        "discount": Decimal("0"),
        "total": Decimal("12000"),
        "payment_method": "CASH",
        "paid": Decimal("20000"),
        "change": Decimal("8000"),
    })()


def test_receipt_uses_logged_in_user_name():
    printer.set_current_cashier(_User("Jajang Suryana"))
    html = printer.receipt_html(_sale(), [], {"store_name": "TOKO SAPNI"})
    raw = printer._escpos_receipt_bytes(
        "TOKO SAPNI", "Alamat", "", _sale().invoice_no, _sale().created_at, [],
        Decimal("12000"), Decimal("0"), Decimal("12000"), "CASH",
        Decimal("20000"), Decimal("8000"), "Terima kasih",
    )
    assert "Kasir: Jajang Suryana" in html
    assert b"Kasir: Jajang Suryana\n" in raw


def test_receipt_cashier_falls_back_to_pengguna():
    printer.set_current_cashier(_User(""))
    html = printer.receipt_html(_sale(), [], {})
    raw = printer._escpos_receipt_bytes(
        "TOKO SEMBAKO", "", "", _sale().invoice_no, _sale().created_at, [],
        Decimal("12000"), Decimal("0"), Decimal("12000"), "CASH",
        Decimal("20000"), Decimal("8000"), "Terima kasih",
    )
    assert "Kasir: Pengguna" in html
    assert b"Kasir: Pengguna\n" in raw
