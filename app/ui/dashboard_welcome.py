from PySide6.QtWidgets import QLabel


def apply_dashboard_welcome(window):
    """Replace the legacy dashboard branding strip with a compact welcome header."""
    stack = getattr(window, "modern_stack", None)
    if stack is None or stack.count() == 0:
        return

    dashboard = stack.widget(0)
    if dashboard is None or dashboard.layout() is None:
        return

    header = dashboard.layout().itemAt(0).widget()
    if header is None:
        return

    header.setObjectName("dashboardWelcomeHeader")
    title = header.findChild(QLabel, "pageTitle")
    subtitle = header.findChild(QLabel, "pageSubtitle")
    if title is not None:
        title.setText("Selamat datang, Admin")
    if subtitle is not None:
        subtitle.setText("Senin, 12 September 2026")

    # Keep this dashboard-only header neutral in both official themes.
    theme = str(getattr(window, "_wpos_active_theme", "DARK")).upper()
    if theme == "LIGHT":
        header.setStyleSheet(
            "#dashboardWelcomeHeader { background:#ffffff; border:1px solid #c8d1d9; "
            "border-radius:12px; padding:8px 14px; }"
            "#dashboardWelcomeHeader QLabel#pageTitle { color:#263442; font-size:22px; font-weight:800; }"
            "#dashboardWelcomeHeader QLabel#pageSubtitle { color:#667583; font-size:12px; }"
        )
    else:
        header.setStyleSheet(
            "#dashboardWelcomeHeader { background:#242a33; border:1px solid #39414c; "
            "border-radius:12px; padding:8px 14px; }"
            "#dashboardWelcomeHeader QLabel#pageTitle { color:#e6eaf0; font-size:22px; font-weight:800; }"
            "#dashboardWelcomeHeader QLabel#pageSubtitle { color:#aab3c0; font-size:12px; }"
        )
    header.show()
