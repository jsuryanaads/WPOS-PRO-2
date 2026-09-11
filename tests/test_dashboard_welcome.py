from datetime import datetime

from PySide6.QtWidgets import QApplication, QLabel, QStackedWidget, QVBoxLayout, QWidget

from app.ui.dashboard_welcome import WEEKDAYS_ID, apply_dashboard_welcome


def test_dashboard_welcome_is_dynamic_and_theme_aware():
    app = QApplication.instance() or QApplication([])
    window = QWidget()
    stack = QStackedWidget(window)
    dashboard = QWidget()
    layout = QVBoxLayout(dashboard)
    header = QWidget()
    header_layout = QVBoxLayout(header)
    header_title = QLabel("Dashboard")
    header_title.setObjectName("pageTitle")
    header_subtitle = QLabel("Legacy welcome")
    header_subtitle.setObjectName("pageSubtitle")
    header_layout.addWidget(header_title)
    header_layout.addWidget(header_subtitle)
    layout.addWidget(header)
    stack.addWidget(dashboard)
    window.modern_stack = stack
    window._wpos_active_theme = "LIGHT"

    apply_dashboard_welcome(window)
    app.processEvents()

    now = datetime.now()
    assert header.objectName() == "dashboardWelcomeHeader"
    assert header_title.text() == "Selamat datang, Admin"
    assert header_subtitle.text() == f"{WEEKDAYS_ID[now.weekday()]}, {now:%d %B %Y}"
    assert "background:#ffffff" in header.styleSheet()
