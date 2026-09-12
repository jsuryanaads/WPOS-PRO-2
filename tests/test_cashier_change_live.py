from pathlib import Path

from app.config import APP_VERSION


ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "app" / "main.py"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"


def test_cashier_payment_change_updates_live():
    source = MAIN.read_text(encoding="utf-8")
    assert "paid.valueChanged.connect(lambda _value: window.update_change())" in source
    assert "window._wpos_paid_change_live = True" in source
    assert "window.update_change()" in source


def test_cashier_change_fix_is_documented_and_versioned():
    config = (ROOT / "app" / "config.py").read_text(encoding="utf-8")
    assert f'APP_VERSION = "{APP_VERSION}"' in config

    readme = README.read_text(encoding="utf-8")
    assert f"Perubahan terbaru {APP_VERSION}" in readme

    changelog = CHANGELOG.read_text(encoding="utf-8")
    assert "## 2.9.2 — Cashier Payment Label Runtime Fix" in changelog
    assert "runtime halaman **Kasir**" in changelog
    assert "Regression test" in changelog
