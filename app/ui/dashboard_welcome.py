from datetime import datetime, timedelta
from decimal import Decimal

from PySide6.QtWidgets import QLabel

from ..database import SessionLocal
from ..services.reports import sales_summary


WEEKDAYS_ID = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu")


def apply_dashboard_welcome(window):
    """Refresh Dashboard metrics without overwriting the global Headerbar.

    Headerbar owns page title, store identity, logged-in display name and date.
    This layer only handles Dashboard-specific legacy cleanup and daily KPIs.
    """
    stack = getattr(window, "modern_stack", None)
    if stack is None or stack.count() == 0:
        return
    dashboard = stack.widget(0)
    if dashboard is None or dashboard.layout() is None:
        return

    now = datetime.now()

    # Hide the legacy page header/branding widget inside the Dashboard.
    first_item = dashboard.layout().itemAt(0)
    legacy_header = first_item.widget() if first_item is not None else None
    if legacy_header is not None:
        legacy_header.setProperty("wposLegacyDashboardHeader", True)
        legacy_header.hide()

    # TRANSAKSI and OMZET are explicitly daily metrics; SALDO KAS remains running balance.
    start = datetime(now.year, now.month, now.day)
    end = start + timedelta(days=1)
    with SessionLocal() as session:
        summary = sales_summary(session, start, end)
    for label in dashboard.findChildren(QLabel):
        if label.objectName() != "cardTitle":
            continue
        if label.text() in {"TRANSAKSI", "TRANSAKSI HARI INI"}:
            label.setText("TRANSAKSI HARI INI")
            value = label.parentWidget().findChild(QLabel, "cardValue")
            if value is not None:
                value.setText(str(summary["transactions"]))
        elif label.text() in {"OMZET", "OMZET HARI INI"}:
            label.setText("OMZET HARI INI")
            value = label.parentWidget().findChild(QLabel, "cardValue")
            if value is not None:
                value.setText(f"Rp {Decimal(str(summary['omzet'])):,.0f}".replace(",", "."))

    dashboard.setProperty("wposDashboardMetricsDate", start.isoformat())
