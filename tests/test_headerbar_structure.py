from pathlib import Path


def test_headerbar_has_three_requested_zones():
    source = Path("app/ui/modern_main_window.py").read_text(encoding="utf-8")
    assert "self.modern_context" in source
    assert "self.modern_hint" in source
    assert 'QLabel(f"Selamat datang, {self.user.username}")' in source
    assert 'setObjectName("modernWelcome")' in source
    assert 'setObjectName("modernDate")' in source
    assert "month_names" in source
    assert 'QLabel("OFFLINE")' not in source
    assert 'QLabel("DATABASE LOKAL")' not in source


def test_headerbar_theme_defines_welcome_and_date_styles():
    source = Path("app/ui/theme_shell.py").read_text(encoding="utf-8")
    assert "QLabel#modernWelcome" in source
    assert "QLabel#modernDate" in source
    assert "min-height:58px" in source
    assert "max-height:64px" in source
