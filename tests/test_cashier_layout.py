from pathlib import Path


def test_cashier_payment_panel_has_compact_geometry_contract():
    source = Path("app/ui/cashier_structure.py").read_text(encoding="utf-8")

    assert 'pay_card.setMinimumWidth(290)' in source
    assert 'pay_card.setMaximumWidth(330)' in source
    assert 'pay_card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)' in source
    assert 'pay_layout.setSpacing(8)' in source
    assert 'item.spacerItem() is not None' in source


def test_cashier_keeps_existing_payment_methods():
    source = Path("app/ui/premium_cashier.py").read_text(encoding="utf-8")

    for method in ("CASH", "QRIS", "TRANSFER", "DEBIT"):
        assert method in source


def test_numeric_spinboxes_explicitly_disable_clear_button():
    source = Path("app/ui/global_ui.py").read_text(encoding="utf-8")

    assert 'line_edit = widget.lineEdit()' in source
    assert 'line_edit.setClearButtonEnabled(False)' in source
    assert 'wposClearButtonDisabled' in source
