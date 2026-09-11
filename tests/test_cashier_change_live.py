from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "app" / "main.py"
README = ROOT / "README.md"
CONFIG = ROOT / "app" / "config.py"
INSTALLER = ROOT / "installer.iss"


def test_cashier_payment_change_updates_live():
    source = MAIN.read_text(encoding="utf-8")
    assert "paid.valueChanged.connect(lambda _value: window.update_change())" in source
    assert "window._wpos_paid_change_live = True" in source
    assert "window.update_change()" in source


def test_cashier_change_fix_is_documented_and_versioned():
    assert 'APP_VERSION = "2.7.3"' in CONFIG.read_text(encoding="utf-8")
    assert '#define MyAppVersion "2.7.3"' in INSTALLER.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")
    assert "### 2.7.3" in readme
    assert "Kembalian Kasir agar live" in readme
