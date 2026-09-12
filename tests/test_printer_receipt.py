from decimal import Decimal

from app.services.printer import _item_lines, receipt_html


def test_thermal_item_line_reserves_both_separators_and_keeps_amount():
    line = _item_lines("ROKO", Decimal("1.0"), Decimal("30000"), Decimal("30000"), 32)[0]

    assert len(line) == 32
    assert "1 x 30,000" in line
    assert line.endswith("30,000")
    assert "30,00" not in line
    assert "1.0" not in line


def test_thermal_item_line_does_not_clip_common_five_digit_amounts():
    line = _item_lines("Indomie", Decimal("2.0"), Decimal("3500"), Decimal("7000"), 32)[0]

    assert len(line) == 32
    assert line.endswith("7,000")
    assert "2 x 3,500" in line


def test_html_receipt_quantity_is_integer_safe():
    class Sale:
        invoice_no = "INV-TEST"
        created_at = __import__("datetime").datetime(2026, 9, 12, 19, 42, 0)
        subtotal = Decimal("30000")
        discount = Decimal("0")
        total = Decimal("30000")
        payment_method = "CASH"
        paid = Decimal("50000")
        change = Decimal("20000")

    html = receipt_html(
        Sale(),
        [{"name": "ROKO", "quantity": Decimal("1.0"), "unit_price": Decimal("30000"), "line_total": Decimal("30000")}],
        {"store_name": "TOKO SAPNI", "store_address": "Jl. Ciawitali No 07", "store_phone": "0851", "receipt_footer": "Terima kasih"},
    )

    assert "1 x 30,000" in html
    assert "1.0 x 30,000" not in html
