from pathlib import Path


def test_login_structure_has_identity_fields_and_offline_mode():
    text = Path("app/ui/login.py").read_text(encoding="utf-8")
    assert "loginLogo" in text
    assert "loginTitle" in text
    assert "loginSubtitle" in text
    assert "loginWelcome" in text
    assert "loginMode" in text
    assert "Offline  •  Database Lokal" in text
    assert "Masukkan username" in text
    assert "Masukkan password" in text
    assert 'QPushButton("MASUK")' in text
    assert "setDefault(True)" in text
    assert "APP_VERSION" not in text
    assert "loginVersion" not in text
    assert "Point of Sale" in text


def test_login_keeps_authentication_flow():
    text = Path("app/ui/login.py").read_text(encoding="utf-8")
    assert "from ..services.auth import login" in text
    assert "with SessionLocal() as session:" in text
    assert "user = login(session, username, password)" in text
    assert "self.on_success(user)" in text


def test_login_version_is_reserved_for_footer():
    login_text = Path("app/ui/login.py").read_text(encoding="utf-8")
    footer_text = Path("app/ui/global_ui.py").read_text(encoding="utf-8")
    assert "APP_VERSION" not in login_text
    assert "APP_VERSION" in footer_text
