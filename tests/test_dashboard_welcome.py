from PySide6.QtWidgets import QApplication, QLabel, QStackedWidget, QVBoxLayout, QWidget

from app.ui import dashboard_welcome


def test_dashboard_welcome_uses_modern_shell_and_hides_legacy_header(monkeypatch):
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

    class FakeSession:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    monkeypatch.setattr(dashboard_welcome, "SessionLocal", lambda: FakeSession())
    monkeypatch.setattr(
        dashboard_welcome,
        "sales_summary",
        lambda session, start, end: {"transactions": 0, "omzet": 0},
    )

    apply_dashboard_welcome = dashboard_welcome.apply_dashboard_welcome
    apply_dashboard_welcome(window)
    app.processEvents()

    assert not legacy_header.isVisible()
    assert window.modern_context.text() == original_context
    assert window.modern_hint.text() == original_hint
    assert legacy_header.property("wposLegacyDashboardHeader") is True
    assert dashboard.property("wposDashboardMetricsDate") is not None
