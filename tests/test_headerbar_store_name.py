from pathlib import Path


def test_headerbar_module_uses_store_name_and_indonesian_date():
    text = Path("app/ui/headerbar.py").read_text(encoding="utf-8")
    assert 'settings.get("store_name")' in text
    assert 'settings.get("store_address")' in text
    assert "Selamat datang" not in text
    assert "_MONTHS" in text
    assert '"Januari"' in text
    assert '"September"' in text
    assert '"Desember"' in text
    assert "_format_date" in text
    assert "_user_display_name" in text


def test_headerbar_is_applied_by_startup():
    text = Path("app/main.py").read_text(encoding="utf-8")
    assert "from .ui.headerbar import apply_headerbar" in text
    assert "apply_headerbar(window)" in text


def test_version_and_docs_are_synchronized():
    from app.config import APP_VERSION
    config = Path("app/config.py").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    assert f'APP_VERSION = "{APP_VERSION}"' in config
    assert f'MyAppVersion "{APP_VERSION}"' in installer
    assert f"Versi aplikasi: **{APP_VERSION}**" in readme
