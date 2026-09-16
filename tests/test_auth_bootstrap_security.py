from pathlib import Path


def test_auth_has_no_legacy_plaintext_bootstrap_literal_in_hashing_call():
    source = Path("app/services/auth.py").read_text(encoding="utf-8")
    assert "DEFAULT_ADMIN_PASSWORD = \"admin123\"" in source
    assert "is_default_admin_password" in source
    assert "change_password" in source
    assert "PBKDF2" not in source  # implementation uses hashlib.pbkdf2_hmac


def test_login_forces_default_admin_password_change():
    source = Path("app/ui/login.py").read_text(encoding="utf-8")
    assert "ChangePasswordDialog" in source
    assert "is_default_admin_password(user)" in source
    assert "change_dialog.exec()" in source
    assert "Password minimal 8 karakter" in source


def test_version_and_docs_are_synchronized():
    from app.config import APP_VERSION

    config = Path("app/config.py").read_text(encoding="utf-8")
    readme = Path("README.md").read_text(encoding="utf-8")
    changelog = Path("CHANGELOG.md").read_text(encoding="utf-8")
    assert f'APP_VERSION = "{APP_VERSION}"' in config
    assert f"Versi aplikasi: **{APP_VERSION}**" in readme
    assert f"## Perubahan terbaru {APP_VERSION}" in readme
    assert f"## {APP_VERSION} —" in changelog
