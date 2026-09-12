from pathlib import Path


def test_purchase_page_is_wired_to_current_purchase_service():
    source = Path("app/ui/main_window.py").read_text(encoding="utf-8")
    assert "def purchase_page(self):" in source
    assert "def save_purchase(self):" in source
    assert "create_purchase" in source
    assert "Pembelian Barang" in source
    assert "Simpan Pembelian & Tambah Stok" in source


def test_version_is_current_release():
    config = Path("app/config.py").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.10.0"' in config
    assert '#define MyAppVersion "2.10.0"' in installer
    assert "Versi aplikasi: **2.10.0**" in readme
    assert "## 2.10.0 — Role-Based Access Control" in changelog
