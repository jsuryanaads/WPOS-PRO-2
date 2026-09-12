from pathlib import Path


def test_headerbar_module_uses_store_name_and_indonesian_weekday():
    text = Path("app/ui/headerbar.py").read_text(encoding="utf-8")
    assert 'settings.get("store_name")' in text
    assert "Selamat datang" not in text
    assert '"Senin"' in text
    assert '"Sabtu"' in text
    assert 'setText(_store_name(window))' in text


def test_headerbar_is_applied_by_startup():
    text = Path("app/main.py").read_text(encoding="utf-8")
    assert "from .ui.headerbar import apply_headerbar" in text
    assert "apply_headerbar(window)" in text


def test_version_and_docs_are_synchronized():
    assert 'APP_VERSION = "2.7.10"' in Path("app/config.py").read_text(encoding="utf-8")
    assert 'MyAppVersion "2.7.10"' in Path("installer.iss").read_text(encoding="utf-8")
    assert "Versi aplikasi: **2.7.10**" in Path("README.md").read_text(encoding="utf-8")
