from pathlib import Path

from app.config import APP_VERSION


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "app" / "main.py"
README = ROOT / "README.md"


def test_cashier_payment_change_updates_live():
    source = MAIN.read_text(encoding="utf-8")
    assert "paid.valueChanged.connect(lambda _value: window.update_change())" in source
    assert "window._wpos_paid_change_live = True" in source
    assert "window.update_change()" in source


def test_cashier_change_fix_is_documented_and_versioned():
    config = (ROOT / "app" / "config.py").read_text(encoding="utf-8")
    assert f'APP_VERSION = "{APP_VERSION}"' in config
    readme = README.read_text(encoding="utf-8")
    assert f"### {APP_VERSION}" in readme
    assert "Kembalian Kasir agar live" in readme
