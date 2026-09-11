from datetime import datetime, timedelta
from decimal import Decimal

from PySide6.QtWidgets import QLabel

from ..database import SessionLocal
from ..services.reports import sales_summary


WEEKDAYS_ID = ("Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu")


def apply_dashboard_welcome(window):
    """Use the modern shell topbar for Dashboard welcome information."""
    stack = getattr(window, "modern_stack", None)
    if stack is None or stack.count() == 0:
        return
    dashboard = stack.widget(0)
    if dashboard is None or dashboard.layout() is None:
        return

    now = datetime.now()
    username = str(getattr(getattr(window, "user", None), "username", "Admin")) or "Admin"
    welcome = f"Selamat datang, {username}"
    date_text = f"{WEEKDAYS_ID[now.weekday()]}, {now:%d %B %Y}"

    # The modern shell already owns the Dashboard header. Reusing it avoids
    # the duplicate/blank legacy header that previously consumed dashboard space.
    context = getattr(window, "modern_context", None)
    hint = getattr(window, "modern_hint", None)
    if context is not None:
        context.setText(welcome)
    if hint is not None:
        hint.setText(date_text)

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
    dashboard.setProperty("wposDashboardWelcome", welcome)
    dashboard.setProperty("wposDashboardDate", date_text)
