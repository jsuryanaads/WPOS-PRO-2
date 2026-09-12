from pathlib import Path


def test_multi_item_purchase_ui_has_basket_workflow():
    source = Path("app/ui/purchase_multi.py").read_text(encoding="utf-8")
    assert "window.purchase_items = []" in source
    assert "def add_purchase_item(window):" in source
    assert "def remove_purchase_item(window, row_index):" in source
    assert "def refresh_purchase_table(window):" in source
    assert "create_purchase(session, items" in source
    assert "SIMPAN PEMBELIAN & TAMBAH STOK" in source


def test_multi_item_purchase_delegates_to_purchase_service():
    source = Path("app/ui/purchase_multi.py").read_text(encoding="utf-8")
    assert "from ..services.purchases import create_purchase" in source
    assert '"product_id": row["product_id"]' in source
    assert '"quantity": row["quantity"]' in source
    assert '"unit_cost": row["unit_cost"]' in source


def test_main_wires_multi_item_purchase_methods():
    source = Path("app/main.py").read_text(encoding="utf-8")
    assert "from .ui.purchase_multi import" in source
    assert "MainWindow.purchase_page = multi_item_purchase_page" in source
    assert "MainWindow.add_purchase_item = multi_item_add_purchase_item" in source
    assert "MainWindow.save_purchase = multi_item_save_purchase" in source


def test_version_is_290():
    config = Path("app/config.py").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.9.0"' in config
    assert '#define MyAppVersion "2.9.0"' in installer
    assert "Versi aplikasi: **2.9.0**" in readme
    assert "## 2.9.0 — Multi-Item Purchase" in changelog
