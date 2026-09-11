from datetime import datetime, timedelta
from decimal import Decimal

from PySide6.QtWidgets import QLabel

from ..database import SessionLocal
from ..services.reports import sales_summary


WEEKDAYS_ID = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu")


def apply_dashboard_welcome(window):
    """Apply a dynamic dashboard welcome header and correct daily KPI values."""
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
    now = datetime.now()
    username = str(getattr(getattr(window, "user", None), "username", "Admin")) or "Admin"
    if title is not None:
        title.setText(f"Selamat datang, {username}")
    if subtitle is not None:
        subtitle.setText(f"{WEEKDAYS_ID[now.weekday()]}, {now:%d %B %Y}")

    # TRANSAKSI and OMZET are explicitly daily metrics; SALDO KAS remains running balance.
    start = datetime(now.year, now.month, now.day)
    end = start + timedelta(days=1)
    with SessionLocal() as session:
        summary = sales_summary(session, start, end)
    for label in dashboard.findChildren(QLabel):
        if label.objectName() != "cardTitle":
            continue
        if label.text() == "TRANSAKSI":
            label.setText("TRANSAKSI HARI INI")
            value = label.parentWidget().findChild(QLabel, "cardValue")
            if value is not None:
                value.setText(str(summary["transactions"]))
        elif label.text() == "OMZET":
            label.setText("OMZET HARI INI")
            value = label.parentWidget().findChild(QLabel, "cardValue")
            if value is not None:
                value.setText(f"Rp {Decimal(str(summary['omzet'])):,.0f}".replace(",", "."))
    dashboard.setProperty("wposDashboardMetricsDate", start.isoformat())

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
