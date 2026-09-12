from pathlib import Path


def test_multi_item_purchase_is_wired():
    source = Path("app/ui/main_window.py").read_text(encoding="utf-8")
    assert "MainWindow.purchase_page = multi_item_purchase_page" in source
    assert "MainWindow.add_purchase_item = multi_item_add_purchase_item" in source
    assert "MainWindow.save_purchase = multi_item_save_purchase" in source


def test_version_is_current_release():
    config = Path("app/config.py").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.10.0"' in config
    assert '#define MyAppVersion "2.10.0"' in installer
    assert "Versi aplikasi: **2.10.0**" in readme
    assert "## 2.10.0 — Role-Based Access Control" in changelog
