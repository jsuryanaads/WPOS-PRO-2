from pathlib import Path


def test_raw_receipt_safety_helpers_are_present():
    source = Path("app/main.py").read_text(encoding="utf-8")
    assert "add_raw_top_safe_area" in source


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
