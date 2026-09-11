from PySide6.QtWidgets import QApplication, QLabel, QStackedWidget, QVBoxLayout, QWidget

from app.ui.dashboard_welcome import apply_dashboard_welcome


def test_dashboard_welcome_replaces_legacy_header():
    app = QApplication.instance() or QApplication([])
    window = QWidget()
    stack = QStackedWidget(window)
    dashboard = QWidget()
    layout = QVBoxLayout(dashboard)
    title = QLabel("Dashboard")
    title.setObjectName("pageTitle")
    subtitle = QLabel("Legacy welcome")
    subtitle.setObjectName("pageSubtitle")
    layout.addWidget(QWidget())
    layout.addWidget(title)
    layout.addWidget(subtitle)
    stack.addWidget(dashboard)
    window.modern_stack = stack
    window._wpos_active_theme = "LIGHT"

    # The production header is the first layout widget; use a compact header
    # harness matching the dashboard page_header structure.
    header = layout.takeAt(0).widget()
    header.deleteLater()
    header = QWidget()
    header_layout = QVBoxLayout(header)
    header_title = QLabel("Dashboard")
    header_title.setObjectName("pageTitle")
    header_subtitle = QLabel("Legacy welcome")
    header_subtitle.setObjectName("pageSubtitle")
    header_layout.addWidget(header_title)
    header_layout.addWidget(header_subtitle)
    layout.insertWidget(0, header)

    apply_dashboard_welcome(window)
    app.processEvents()

    assert header.objectName() == "dashboardWelcomeHeader"
    assert header_title.text() == "Selamat datang, Admin"
    assert header_subtitle.text() == "Senin, 12 September 2026"
    assert "background:#ffffff" in header.styleSheet()
