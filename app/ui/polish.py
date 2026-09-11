from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QLabel, QFrame, QHBoxLayout, QStatusBar, QTableWidget, QTableWidgetItem

from ..config import APP_NAME, APP_VERSION
from .branding import LOGO_PATH


FOOTER_TEXT = f"{APP_NAME} | v{APP_VERSION} | {datetime.now().year} | by Jsuryana"


def _set_dashboard_empty_state(table, message):
    """Show a compact empty state without changing dashboard data semantics."""
    if table.rowCount() != 0:
        return
    table.setRowCount(1)
    item = QTableWidgetItem(message)
    item.setTextAlignment(Qt.AlignCenter)
    table.setItem(0, 0, item)
    if table.columnCount() > 1:
        table.setSpan(0, 0, 1, table.columnCount())


def apply_ui_polish(window):
    """Apply theme-neutral presentation refinements to legacy and modern shells."""
    if window.statusBar() is None:
        window.setStatusBar(QStatusBar(window))

    # Modern V2 already renders the branded application footer inside its
    # content area. The legacy QStatusBar would otherwise create a duplicate
    # information strip at the very bottom of the window.
    if hasattr(window, "modern_stack"):
        window.statusBar().hide()
        window.setWindowTitle(APP_NAME)
    else:
        window.statusBar().showMessage(FOOTER_TEXT)
        window.setWindowTitle(APP_NAME)

    tabs = getattr(window, "tabs", None)
    if tabs is not None and hasattr(tabs, "tabBar"):
        bar = tabs.tabBar()
        bar.setExpanding(False)
        bar.setUsesScrollButtons(True)
        bar.setElideMode(Qt.ElideRight)
        bar.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold))

    for table in window.findChildren(QTableWidget):
        table.setShowGrid(False)
        table.setWordWrap(False)
        table.setMinimumHeight(180)
        table.verticalHeader().setDefaultSectionSize(32)
        table.setFont(QFont("Segoe UI", 9))

    # The dashboard should communicate an empty local database clearly rather
    # than leaving large blank table surfaces when there is no transaction or
    # low-stock data yet. This is presentation-only and does not create data.
    if hasattr(window, "modern_stack") and window.modern_stack.count() > 0:
        dashboard = window.modern_stack.widget(0)
        if dashboard is not None:
            sales_table = dashboard.findChild(QTableWidget, "dashboard_sales")
            low_table = dashboard.findChild(QTableWidget, "dashboard_low")
            if sales_table is not None:
                _set_dashboard_empty_state(sales_table, "Belum ada transaksi")
            if low_table is not None:
                _set_dashboard_empty_state(low_table, "Tidak ada stok yang perlu diperhatikan")

    # The Modern POS 2026 shell already has its own branded sidebar.
    # Only add the legacy Dashboard brand strip when a real QTabWidget is present.
    if (
        tabs is not None
        and hasattr(tabs, "count")
        and hasattr(tabs, "widget")
        and LOGO_PATH.exists()
        and tabs.count() > 0
    ):
        dashboard = tabs.widget(0)
        layout = dashboard.layout()
        existing = dashboard.findChildren(QFrame, "brandStrip")
        if existing or layout is None:
            return

        strip = QFrame()
        strip.setObjectName("brandStrip")
        row = QHBoxLayout(strip)
        row.setContentsMargins(14, 9, 14, 9)

        logo = QLabel()
        logo.setObjectName("brandLogo")
        pix = QPixmap(str(LOGO_PATH))
        if not pix.isNull():
            logo.setPixmap(pix.scaledToHeight(42, Qt.SmoothTransformation))

        name = QLabel(APP_NAME)
        name.setObjectName("brandName")
        version = QLabel(f"{APP_VERSION}  ·  Point of Sale")
        version.setObjectName("brandVersion")

        row.addWidget(logo)
        row.addSpacing(10)
        text = QHBoxLayout()
        text.setContentsMargins(0, 0, 0, 0)
        text.addWidget(name)
        text.addSpacing(8)
        text.addWidget(version)
        text.addStretch()
        row.addLayout(text)
        layout.insertWidget(0, strip)
