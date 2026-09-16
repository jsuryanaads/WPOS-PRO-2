from pathlib import Path


def test_product_display_is_applied_by_startup():
    text = Path("app/main.py").read_text(encoding="utf-8")
    assert "from .ui.product_display import apply_product_table_display" in text
    assert "apply_product_table_display(window)" in text


def test_version_and_docs_are_synchronized():
    from app.config import APP_VERSION
    config = Path("app/config.py").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    assert f'APP_VERSION = "{APP_VERSION}"' in config
    assert f'Versi aplikasi: **{APP_VERSION}**' in readme
    assert f'#define MyAppVersion "{APP_VERSION}"' in installer
