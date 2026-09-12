from pathlib import Path


def test_product_display_normalizes_whole_stock_and_has_status():
    text = Path("app/ui/product_display.py").read_text(encoding="utf-8")
    assert "_whole_number" in text
    assert '"AKTIF"' in text
    assert '"NONAKTIF"' in text
    assert '"Status"' in text
    assert 'Decimal("1")' in text


def test_product_display_refreshes_after_navigation():
    text = Path("app/ui/product_display.py").read_text(encoding="utf-8")
    assert "QTimer.singleShot(0" in text
    assert "currentChanged.connect(refresh_after_navigation)" in text


def test_main_applies_product_table_display():
    text = Path("app/main.py").read_text(encoding="utf-8")
    assert "from .ui.product_display import apply_product_table_display" in text
    assert "apply_product_table_display(window)" in text


def test_version_and_docs_are_synchronized():
    config = Path("app/config.py").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.7.10"' in config
    assert 'Versi aplikasi: **2.7.10**' in readme
    assert '### 2.7.10' in readme
    assert '#define MyAppVersion "2.7.10"' in installer
