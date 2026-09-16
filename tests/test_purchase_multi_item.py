from pathlib import Path


def test_purchase_multi_item_ui_contract():
    source = Path("app/ui/purchase_multi.py").read_text(encoding="utf-8")
    assert "Simpan Pembelian & Tambah Stok" in source


def test_version_is_current_release():
    from app.config import APP_VERSION
    config = Path("app/config.py").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert f'APP_VERSION = "{APP_VERSION}"' in config
    assert f'#define MyAppVersion "{APP_VERSION}"' in installer
    assert f"Versi aplikasi: **{APP_VERSION}**" in readme
    assert f"## {APP_VERSION} —" in changelog
