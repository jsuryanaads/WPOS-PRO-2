from PySide6.QtWidgets import QApplication, QLabel, QStackedWidget, QVBoxLayout, QWidget

from app.ui.dashboard_welcome import apply_dashboard_welcome


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
    original_context = window.modern_context.text()
    original_hint = window.modern_hint.text()

    apply_dashboard_welcome(window)
    app.processEvents()

    assert not legacy_header.isVisible()
    assert window.modern_context.text() == original_context
    assert window.modern_hint.text() == original_hint
    assert legacy_header.property("wposLegacyDashboardHeader") is True
    assert dashboard.property("wposDashboardMetricsDate") is not None
