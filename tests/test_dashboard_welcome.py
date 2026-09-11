from datetime import datetime

from PySide6.QtWidgets import QApplication, QLabel, QStackedWidget, QVBoxLayout, QWidget

from app.ui.dashboard_welcome import WEEKDAYS_ID, apply_dashboard_welcome


def test_dashboard_welcome_uses_modern_shell_and_hides_legacy_header():
    app = QApplication.instance() or QApplication([])
    window = QWidget()
    stack = QStackedWidget(window)
    dashboard = QWidget()
    layout = QVBoxLayout(dashboard)
    legacy_header = QWidget()
    header_layout = QVBoxLayout(legacy_header)
    header_layout.addWidget(QLabel("Legacy logo/header"))
    layout.addWidget(legacy_header)
    stack.addWidget(dashboard)
    window.modern_stack = stack
    window._wpos_active_theme = "LIGHT"
    window.modern_context = QLabel("Dashboard")
    window.modern_hint = QLabel("Ringkasan bisnis hari ini")
    class User:
        username = "Admin"
    window.user = User()

    apply_dashboard_welcome(window)
    app.processEvents()

    now = datetime.now()
    assert not legacy_header.isVisible()
    assert window.modern_context.text() == "Selamat datang, Admin"
    assert window.modern_hint.text() == f"{WEEKDAYS_ID[now.weekday()]}, {now:%d %B %Y}"
    assert dashboard.property("wposDashboardWelcome") == "Selamat datang, Admin"
    assert dashboard.property("wposDashboardDate") == f"{WEEKDAYS_ID[now.weekday()]}, {now:%d %B %Y}"
