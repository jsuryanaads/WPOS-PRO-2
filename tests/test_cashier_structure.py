from pathlib import Path


def test_cashier_structure_module_is_presentation_only():
    source = Path("app/ui/cashier_structure.py").read_text(encoding="utf-8")
    assert "premiumCartCard" in source
    assert "premiumPayCard" in source
    assert "premiumTransactionControls" in source
    assert "Keranjang Transaksi" in source
    assert "BAYAR & CETAK" in source
    assert "SessionLocal" not in source
    assert "create_sale" not in source


def test_main_applies_cashier_structure():
    source = Path("app/main.py").read_text(encoding="utf-8")
    assert "from .ui.cashier_structure import apply_cashier_structure" in source
    assert "apply_cashier_structure(window)" in source


def test_cashier_payment_card_stays_compact():
    source = Path("app/ui/cashier_structure.py").read_text(encoding="utf-8")
    assert 'pay_card.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)' in source
    assert 'pay_layout.setSpacing(8)' in source
    assert 'item.spacerItem() is not None' in source


def test_cashier_payment_value_labels_are_not_redundant():
    source = Path("app/ui/premium_cashier.py").read_text(encoding="utf-8")
    assert 'total_l.addWidget(_label("TOTAL TRANSAKSI", "premiumTotalCaption"))' in source
    assert 'window.total_label = _label("Rp 0", "premiumTotal")' in source
    assert 'change_l.addWidget(_label("KEMBALIAN", "premiumChangeCaption"))' in source
    assert 'window.change_label = _label("Rp 0", "premiumChange")' in source
    assert 'Kembalian: Rp 0' not in source
    assert 'TOTAL Rp 0' not in source


def test_cashier_runtime_reapplies_compact_payment_labels():
    source = Path("app/ui/cashier_structure.py").read_text(encoding="utf-8")
    assert "_install_payment_label_contract" in source
    assert "window.update_change = update_change_with_contract" in source
    assert 'removeprefix("TOTAL ")' in source
    assert 'removeprefix("Kembalian: ")' in source


def test_version_is_293():
    config = Path("app/config.py").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.9.3"' in config
    assert '#define MyAppVersion "2.9.3"' in installer
    assert "Versi aplikasi: **2.9.3**" in readme
    assert "## 2.9.3 — Thermal Receipt Item Formatting Fix" in changelog
