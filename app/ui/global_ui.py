from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGridLayout,
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

from .theme_shell import apply_theme_shell
from .themes import current_theme


GLOBAL_UI_STYLE = """
/* WPOS PRO V2 — unified geometry/UX contract; colors come from the active theme. */
QWidget { font-family: 'Segoe UI'; font-size: 11px; }
QLabel#applicationFooterLabel { font-size: 10px; font-weight: 600; }
QLabel#pageTitle { font-size: 24px; font-weight: 900; }
QLabel#pageSubtitle { font-size: 11px; }

QFrame#card { border-radius: 12px; }
QLabel#cardTitle { font-size: 10px; font-weight: 800; }
QLabel#cardValue { font-size: 22px; font-weight: 900; }
QLabel#total { border-radius: 9px; padding: 10px 14px; font-size: 18px; font-weight: 900; }

QGroupBox { border-radius: 12px; padding: 14px 12px 10px; margin-top: 10px; font-weight: 800; }
QGroupBox::title { subcontrol-origin: margin; left: 14px; top: 2px; padding: 0 7px; }

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { min-height: 32px; max-height: 36px; border-radius: 8px; padding: 3px 9px; }
QSpinBox, QDoubleSpinBox { min-width: 110px; padding-right: 31px; }
QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {
    subcontrol-origin: border;
    width: 24px;
    margin: 1px;
    border-radius: 5px;
}
QSpinBox::up-button, QDoubleSpinBox::up-button { subcontrol-position: top right; }
QSpinBox::down-button, QDoubleSpinBox::down-button { subcontrol-position: bottom right; }
QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover,
QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover { margin: 0px; }
QTextEdit { max-height: 120px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus { border-width: 1px; }

QPushButton { min-height: 34px; max-height: 38px; border-radius: 8px; padding: 6px 14px; font-weight: 800; }
QPushButton:pressed { padding-top: 7px; }

QTableWidget { min-height: 180px; border-radius: 10px; }
QTableWidget::item { padding: 7px; }
QHeaderView::section { min-height: 32px; padding: 8px; border: 0; font-weight: 900; }
QScrollArea { border: 0; background: transparent; }
QScrollBar:vertical { width: 9px; margin: 2px; background: transparent; }

/* Consistent hierarchy for every page */
QWidget[wposPageType="cashier"] QTableWidget { min-height: 250px; }
QWidget[wposPageType="products"] QTableWidget,
QWidget[wposPageType="stock"] QTableWidget,
QWidget[wposPageType="reports"] QTableWidget { min-height: 280px; }
QWidget[wposPageType="master"] QTableWidget { min-height: 260px; }
QWidget[wposPageType="purchase"] QTableWidget { min-height: 240px; }
QWidget[wposPageType="cash"] QTableWidget { min-height: 240px; }
QWidget[wposPageType="settings"] QGroupBox,
QWidget[wposPageType="printer"] QGroupBox,
QWidget[wposPageType="backup"] QGroupBox { max-width: 900px; }

/* Responsive geometry: avoid oversized forms/cards and preserve usable space. */
QWidget[wposPage="true"] QGroupBox { max-width: 1100px; }
QWidget[wposPage="true"] QTableWidget { max-width: 1400px; }
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


def _hide_duplicate_page_headers(root):
    """The modern shell owns the page title; legacy page headers are hidden."""
    stack = getattr(root, "modern_stack", None)
    if stack is None:
        return
    for index in range(stack.count()):
        page = stack.widget(index)
        if page is None or page.objectName() == "premiumCashierPage":
            continue
        layout = page.layout()
        if layout is None:
            continue
        for position in range(layout.count()):
            item = layout.itemAt(position)
            widget = item.widget() if item else None
            if widget is None:
                continue
            if widget.findChild(QLabel, "pageTitle") and widget.findChild(QLabel, "pageSubtitle"):
                widget.hide()
                break


def _normalize_layouts(root):
    """Apply one compact, predictable geometry contract to every page."""
    _hide_duplicate_page_headers(root)

    stack = getattr(root, "modern_stack", None)
    if stack is not None:
        for index in range(stack.count()):
            page = stack.widget(index)
            if page is None or page.layout() is None:
                continue
            layout = page.layout()
            layout.setSpacing(min(max(layout.spacing(), 8), 12))
            layout.setContentsMargins(16, 8, 16, 12)
            page.setProperty("wposLayoutReady", True)

    for form in root.findChildren(QFormLayout):
        form.setRowWrapPolicy(QFormLayout.DontWrapRows)
        form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(5)
        parent = form.parentWidget()
        if isinstance(parent, QGroupBox):
            rows = form.rowCount()
            required = 26 + (rows * 32) + (max(0, rows - 1) * 5) + 8
            parent.setMinimumHeight(max(0, required))
            parent.setMaximumWidth(1100)

    for grid in root.findChildren(QGridLayout):
        grid.setHorizontalSpacing(min(max(grid.horizontalSpacing(), 10), 16))
        grid.setVerticalSpacing(min(max(grid.verticalSpacing(), 8), 12))


def _normalize_controls(root):
    for table in root.findChildren(QTableWidget):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setWordWrap(False)
        table.setSizeAdjustPolicy(QAbstractItemView.AdjustIgnored)
        table.verticalHeader().setVisible(False)
        table.verticalHeader().setDefaultSectionSize(34)
        header = table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        header.setMinimumSectionSize(70)
        for column in range(table.columnCount()):
            header.setSectionResizeMode(column, QHeaderView.Interactive)
        if table.columnCount() > 0:
            header.setSectionResizeMode(table.columnCount() - 1, QHeaderView.Stretch)

    for widget_type in (QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit):
        for widget in root.findChildren(widget_type):
            widget.setFocusPolicy(Qt.StrongFocus)
            if isinstance(widget, QLineEdit):
                widget.setClearButtonEnabled(True)
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.setMinimumWidth(max(widget.minimumWidth(), 110))
                widget.setMinimumHeight(max(widget.minimumHeight(), 32))
                widget.setMaximumHeight(max(widget.maximumHeight(), 36))

    for button in root.findChildren(QPushButton):
        button.setCursor(Qt.PointingHandCursor)
        button.setAutoDefault(False)
        button.setDefault(False)

    for group in root.findChildren(QGroupBox):
        group.setContentsMargins(8, 10, 8, 8)

    for scroll in root.findChildren(QScrollArea):
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    for frame in root.findChildren(QFrame, "applicationFooter"):
        frame.setMinimumHeight(28)
        label = frame.findChild(QLabel, "applicationFooterLabel")
        if label:
            label.setAlignment(Qt.AlignCenter)


def apply_global_ui(app, root=None):
    """Apply one geometry/UX contract and then the active theme visual contract."""
    current = app.styleSheet()
    if GLOBAL_UI_STYLE not in current:
        app.setStyleSheet(current + GLOBAL_UI_STYLE)
    if root is None:
        return
    _mark_pages(root)
    _normalize_layouts(root)
    _normalize_controls(root)
    apply_theme_shell(root, current_theme())
    root.style().unpolish(root)
    root.style().polish(root)
    root.update()
