from datetime import datetime

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
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTableWidget,
    QTextEdit,
    QSizePolicy,
)

from ..config import APP_NAME
from .theme_shell import apply_theme_shell
from .themes import current_theme


GLOBAL_UI_STYLE = """
/* WPOS PRO 2 — unified geometry/UX contract for all 14 business pages. */
QWidget { font-family: 'Segoe UI'; font-size: 11px; }
QLabel { background: transparent; }
QFrame#applicationFooter { min-height: 30px; max-height: 30px; }
QLabel#applicationFooterLabel { font-size: 10px; font-weight: 600; }
QLabel#pageTitle { font-size: 24px; font-weight: 900; }
QLabel#pageSubtitle { font-size: 11px; }
QFrame#card { border-radius: 12px; min-width: 145px; max-width: 280px; }
QLabel#cardTitle { font-size: 10px; font-weight: 800; }
QLabel#cardValue { font-size: 22px; font-weight: 900; }
QLabel#total { border-radius: 9px; padding: 10px 14px; font-size: 18px; font-weight: 900; }
QGroupBox { border-radius: 12px; padding: 14px 12px 10px; margin-top: 10px; font-weight: 800; }
QGroupBox::title { subcontrol-origin: margin; left: 14px; top: 2px; padding: 0 7px; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { min-height: 32px; max-height: 36px; border-radius: 8px; padding: 3px 9px; }
QSpinBox, QDoubleSpinBox { min-width: 110px; padding-right: 31px; }
QSpinBox::up-button, QDoubleSpinBox::up-button, QSpinBox::down-button, QDoubleSpinBox::down-button { subcontrol-origin: border; width: 24px; margin: 1px; border-radius: 5px; }
QSpinBox::up-button, QDoubleSpinBox::up-button { subcontrol-position: top right; }
QSpinBox::down-button, QDoubleSpinBox::down-button { subcontrol-position: bottom right; }
QTextEdit { max-height: 120px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus { border-width: 1px; }
QPushButton { min-height: 34px; max-height: 38px; border-radius: 8px; padding: 6px 14px; font-weight: 800; }
QTableWidget { min-height: 180px; border-radius: 10px; }
QTableWidget::item { padding: 7px; }
QHeaderView::section { min-height: 32px; padding: 8px; border: 0; font-weight: 900; }
QScrollArea { border: 0; background: transparent; }
QScrollBar:vertical { width: 9px; margin: 2px; background: transparent; }
QWidget[wposPageType="cashier"] QTableWidget { min-height: 250px; }
QWidget[wposPageType="products"] QTableWidget, QWidget[wposPageType="stock"] QTableWidget, QWidget[wposPageType="reports"] QTableWidget { min-height: 280px; }
QWidget[wposPageType="master"] QTableWidget { min-height: 250px; }
QWidget[wposPageType="purchase"] QTableWidget, QWidget[wposPageType="cash"] QTableWidget { min-height: 240px; }
QWidget[wposPageType="settings"] QGroupBox, QWidget[wposPageType="printer"] QGroupBox, QWidget[wposPageType="backup"] QGroupBox { max-width: 900px; }
QWidget[wposPage="true"] QGroupBox { max-width: 1100px; }
QWidget[wposPage="true"] QTableWidget { max-width: 1400px; }
"""

_PAGE_TYPES = [
    "dashboard", "cashier", "products", "stock", "purchase", "cash", "reports",
    "settings", "printer", "backup", "master", "master", "master", "master",
]


def add_application_footer(window):
    """Add the shared 30px application footer to modern shell or login."""
    parent = window.findChild(QFrame, "modernContent")
    target_layout = parent.layout() if parent is not None else window.layout()
    if target_layout is None or window.findChild(QFrame, "applicationFooter") is not None:
        return
    footer = QFrame()
    footer.setObjectName("applicationFooter")
    footer.setFixedHeight(30)
    footer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    layout = QHBoxLayout(footer)
    layout.setContentsMargins(8, 0, 8, 0)
    layout.setSpacing(0)
    from ..config import APP_VERSION
    label = QLabel(f"{APP_NAME} | v{APP_VERSION} | {datetime.now().year} | by Jsuryana")
    label.setObjectName("applicationFooterLabel")
    label.setAlignment(Qt.AlignCenter)
    label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
    layout.addWidget(label)
    target_layout.addWidget(footer, 0)


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
            if widget is not None and widget.findChild(QLabel, "pageTitle") and widget.findChild(QLabel, "pageSubtitle"):
                widget.hide()
                break


def _normalize_layouts(root):
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
            for child in page.findChildren(QGroupBox):
                child.setMaximumWidth(1100)

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
            parent.setMinimumHeight(26 + (rows * 32) + (max(0, rows - 1) * 5) + 8)
            parent.setMaximumWidth(1100)

    for grid in root.findChildren(QGridLayout):
        grid.setHorizontalSpacing(min(max(grid.horizontalSpacing(), 10), 16))
        grid.setVerticalSpacing(min(max(grid.verticalSpacing(), 8), 12))


def _normalize_controls(root):
    for widget in root.findChildren(QLineEdit):
        widget.setClearButtonEnabled(False)
        widget.setProperty("wposClearButtonDisabled", True)
        widget.setFocusPolicy(Qt.StrongFocus)
        widget.setMinimumHeight(max(widget.minimumHeight(), 32))

    for table in root.findChildren(QTableWidget):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setWordWrap(False)
        table.setSizeAdjustPolicy(QAbstractItemView.AdjustIgnored)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
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

    for widget_type in (QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit):
        for widget in root.findChildren(widget_type):
            widget.setFocusPolicy(Qt.StrongFocus)
            widget.setMinimumHeight(max(widget.minimumHeight(), 32))
            if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.setMinimumWidth(max(widget.minimumWidth(), 110))
                line_edit = widget.lineEdit()
                if line_edit is not None:
                    line_edit.setClearButtonEnabled(False)
                    line_edit.setProperty("wposClearButtonDisabled", True)

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
        frame.setFixedHeight(30)
        label = frame.findChild(QLabel, "applicationFooterLabel")
        if label:
            label.setAlignment(Qt.AlignCenter)


def apply_global_ui(app, root=None):
    """Apply the shared geometry/UX contract, then the active theme."""
    current = app.styleSheet()
    if GLOBAL_UI_STYLE not in current:
        app.setStyleSheet(current + GLOBAL_UI_STYLE)
    if root is None:
        return
    _mark_pages(root)
    _normalize_layouts(root)
    _normalize_controls(root)
    apply_theme_shell(root, current_theme())
    root.setWindowTitle(APP_NAME)
    root.style().unpolish(root)
    root.style().polish(root)
    root.update()
