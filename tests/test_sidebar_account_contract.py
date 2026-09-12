from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAIN_SOURCE = (ROOT / "app" / "main.py").read_text(encoding="utf-8")
MODERN_SOURCE = (ROOT / "app" / "ui" / "modern_main_window.py").read_text(encoding="utf-8")


def test_sidebar_identity_is_hidden_after_global_headerbar_refresh():
    assert '"modernUser", "modernRole"' in MAIN_SOURCE
    assert "label.hide()" in MAIN_SOURCE
    assert '"modernAccount"' in MAIN_SOURCE
    assert '"modernLogout"' in MODERN_SOURCE


def test_sidebar_cleanup_does_not_remove_logout_control():
    assert 'logout = QPushButton("Keluar")' in MODERN_SOURCE
    assert 'logout.clicked.connect(self.logout)' in MODERN_SOURCE
