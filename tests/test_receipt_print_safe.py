from pathlib import Path


def test_raw_receipt_safety_helpers_are_present():
    source = Path("app/main.py").read_text(encoding="utf-8")
    assert "add_raw_top_safe_area" in source


def test_version_is_current_release():
    config = Path("app/config.py").read_text(encoding="utf-8")
    installer = Path("installer.iss").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert 'APP_VERSION = "2.10.0"' in config
    assert '#define MyAppVersion "2.10.0"' in installer
    assert "Versi aplikasi: **2.10.0**" in readme
    assert "## 2.10.0 — Role-Based Access Control" in changelog
