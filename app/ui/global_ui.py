from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QGroupBox,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTableWidget,
    QTextEdit,
)


GLOBAL_UI_STYLE = """
/* WPOS PRO V2 — unified UI/UX contract */
QWidget { font-family: 'Segoe UI'; font-size: 11px; }
QLabel#applicationFooterLabel { font-size: 10px; font-weight: 600; }
QLabel#pageTitle { font-size: 24px; font-weight: 900; color: #0f172a; }
QLabel#pageSubtitle { color: #64748b; font-size: 11px; }

QFrame#card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }
QLabel#cardTitle { color: #64748b; font-size: 10px; font-weight: 800; }
QLabel#cardValue { color: #0f172a; font-size: 22px; font-weight: 900; }
QLabel#total { background: #0f172a; color: #ffffff; border-radius: 9px; padding: 10px 14px; font-size: 18px; font-weight: 900; }

QGroupBox { border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px 12px 12px; margin-top: 12px; background: #ffffff; font-weight: 800; color: #334155; }
QGroupBox::title { subcontrol-origin: margin; left: 14px; top: 2px; padding: 0 7px; background: #ffffff; color: #334155; }

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { min-height: 34px; border-radius: 8px; border: 1px solid #cbd5e1; padding: 4px 9px; background: #ffffff; color: #0f172a; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus { border: 1px solid #2563eb; }
QLineEdit:disabled, QComboBox:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QTextEdit:disabled { background: #f1f5f9; color: #94a3b8; }

QPushButton { min-height: 34px; border-radius: 8px; border: 1px solid #cbd5e1; padding: 7px 14px; background: #ffffff; color: #334155; font-weight: 800; }
QPushButton:hover { background: #eff6ff; border-color: #93c5fd; color: #1d4ed8; }
QPushButton:pressed { padding-top: 8px; }
QPushButton#primary, QPushButton#dashboardPrimary { background: #2563eb; border-color: #2563eb; color: #ffffff; }
QPushButton#primary:hover, QPushButton#dashboardPrimary:hover { background: #1d4ed8; border-color: #1d4ed8; }
QPushButton#danger { background: #dc2626; border-color: #dc2626; color: #ffffff; }
QPushButton#danger:hover { background: #b91c1c; border-color: #b91c1c; }
QPushButton#dashboardSecondary { background: #e2e8f0; color: #0f172a; border-color: #e2e8f0; }
QPushButton#dashboardGhost { background: #ffffff; color: #475569; }

QTableWidget { min-height: 180px; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; gridline-color: #eef2f7; alternate-background-color: #f8fafc; selection-background-color: #dbeafe; selection-color: #0f172a; }
QTableWidget::item { padding: 7px; }
QHeaderView::section { min-height: 32px; padding: 8px; border: 0; border-bottom: 1px solid #e2e8f0; background: #f8fafc; color: #475569; font-weight: 900; }
QScrollArea { border: 0; background: transparent; }
QScrollBar:vertical { width: 9px; margin: 2px; background: transparent; }
QScrollBar::handle:vertical { background: #cbd5e1; border-radius: 4px; min-height: 28px; }
QScrollBar::handle:vertical:hover { background: #94a3b8; }
QToolTip { background: #0f172a; color: #ffffff; border: 0; padding: 6px 8px; }

/* Consistent hierarchy for every rebuilt page */
QWidget[wposPageType="cashier"] QTableWidget { min-height: 250px; }
QWidget[wposPageType="products"] QTableWidget,
QWidget[wposPageType="stock"] QTableWidget,
QWidget[wposPageType="reports"] QTableWidget { min-height: 280px; }
QWidget[wposPageType="master"] QTableWidget { min-height: 300px; }
QWidget[wposPageType="settings"] QGroupBox,
QWidget[wposPageType="printer"] QGroupBox,
QWidget[wposPageType="backup"] QGroupBox { max-width: 900px; }
"""

_PAGE_TYPES = [
    "dashboard", "cashier", "products", "stock", "purchase", "cash", "reports",
    "settings", "printer", "backup", "master", "master", "master", "master",
]


def _mark_pages(root):
    stack = getattr(root, "modern_stack", None)
    if stack is None:
        return
    for index in range(stack.count()):
        page = stack.widget(index)
        if page is None:
            continue
        page.setObjectName(page.objectName() or f"wposPage{index}")
        page.setProperty("wposPage", "true")
        page.setProperty("wposPageType", _PAGE_TYPES[index] if index < len(_PAGE_TYPES) else "master")


def _normalize_controls(root):
    for table in root.findChildren(QTableWidget):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setWordWrap(False)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    for widget_type in (QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit):
        for widget in root.findChildren(widget_type):
            widget.setFocusPolicy(Qt.StrongFocus)
            if isinstance(widget, QLineEdit):
                widget.setClearButtonEnabled(True)

    for button in root.findChildren(QPushButton):
        button.setCursor(Qt.PointingHandCursor)
        button.setAutoDefault(False)
        button.setDefault(False)

    for group in root.findChildren(QGroupBox):
        group.setContentsMargins(8, 12, 8, 8)

    for scroll in root.findChildren(QScrollArea):
        scroll.setWidgetResizable(True)

    for frame in root.findChildren(QFrame, "applicationFooter"):
        frame.setMinimumHeight(28)
        label = frame.findChild(QLabel, "applicationFooterLabel")
        if label:
            label.setAlignment(Qt.AlignCenter)


def apply_global_ui(app, root=None):
    """Apply the single presentation contract while preserving all business logic."""
    current = app.styleSheet()
    if GLOBAL_UI_STYLE not in current:
        app.setStyleSheet(current + GLOBAL_UI_STYLE)
    if root is None:
        return
    _mark_pages(root)
    _normalize_controls(root)
    root.style().unpolish(root)
    root.style().polish(root)
    root.update()
