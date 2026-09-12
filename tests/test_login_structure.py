from pathlib import Path


def test_login_structure_has_identity_fields_and_offline_mode():
    text = Path("app/ui/login.py").read_text(encoding="utf-8")
    assert "loginLogo" in text
    assert "loginTitle" in text
    assert "loginVersion" in text
    assert "loginWelcome" in text
    assert "loginMode" in text
    assert "Offline  •  Database Lokal" in text
    assert "Masukkan username" in text
    assert "Masukkan password" in text
    assert 'QPushButton("MASUK")' in text
    assert "setDefault(True)" in text


def test_login_keeps_authentication_flow():
    text = Path("app/ui/login.py").read_text(encoding="utf-8")
    assert "from ..services.auth import login" in text
    assert "with SessionLocal() as session:" in text
    assert "user = login(session, username, password)" in text
    assert "self.on_success(user)" in text


def test_login_uses_current_app_version():
    text = Path("app/ui/login.py").read_text(encoding="utf-8")
    assert "APP_NAME" in text
    assert "APP_VERSION" in text
    assert 'f"{APP_VERSION}  ·  Point of Sale"' in text
