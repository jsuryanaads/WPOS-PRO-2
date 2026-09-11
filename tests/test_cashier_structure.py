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


def test_version_is_277():
    config = Path("app/config.py").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.7.7"' in config
    assert '#define MyAppVersion "2.7.7"' in installer
    assert "Versi aplikasi: **2.7.7**" in readme
