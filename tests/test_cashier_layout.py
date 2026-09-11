from pathlib import Path


def test_cashier_payment_panel_has_production_safe_geometry():
    source = Path("app/ui/premium_cashier.py").read_text(encoding="utf-8")

    assert 'pay_card.setMinimumWidth(330)' in source
    assert 'checkout = QPushButton("BAYAR & CETAK")' in source
    assert 'checkout.setMinimumWidth(165)' in source
    assert 'clear.setMinimumWidth(76)' in source
    assert 'body.addWidget(pay_card, 0)' in source


def test_cashier_keeps_existing_payment_methods():
    source = Path("app/ui/premium_cashier.py").read_text(encoding="utf-8")

    for method in ("CASH", "QRIS", "TRANSFER", "DEBIT"):
        assert method in source
