from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QGroupBox,
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

QGroupBox { border-radius: 12px; padding: 18px 12px 12px; margin-top: 12px; font-weight: 800; }
QGroupBox::title { subcontrol-origin: margin; left: 14px; top: 2px; padding: 0 7px; }

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { min-height: 34px; border-radius: 8px; padding: 4px 9px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus { border-width: 1px; }

QPushButton { min-height: 34px; border-radius: 8px; padding: 7px 14px; font-weight: 800; }
QPushButton:pressed { padding-top: 8px; }

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


def _hide_duplicate_page_headers(root):
    """The modern shell owns the page title; legacy page headers are hidden.

    Pages built by MainWindow still contain their original page_header() for
    compatibility. Keeping it visible would produce two titles stacked on
    top of each other. This pass only hides a header that contains both the
    canonical pageTitle and pageSubtitle markers; business widgets remain
    untouched.
    """
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
    """Apply one geometry contract to every page layout."""
    _hide_duplicate_page_headers(root)

    stack = getattr(root, "modern_stack", None)
    if stack is not None:
        for index in range(stack.count()):
            page = stack.widget(index)
            if page is None or page.layout() is None:
                continue
            layout = page.layout()
            # Preserve page-specific margins, but enforce a predictable
            # vertical rhythm between top-level content blocks.
            if layout.spacing() < 10:
                layout.setSpacing(10)
            page.setProperty("wposLayoutReady", True)

    for form in root.findChildren(QFormLayout):
        form.setRowWrapPolicy(QFormLayout.DontWrapRows)
        form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        form.setFormAlignment(Qt.AlignLeft | Qt.AlignTop)
        form.setHorizontalSpacing(14)
        form.setVerticalSpacing(7)
        parent = form.parentWidget()
        if isinstance(parent, QGroupBox) and form.rowCount() >= 5:
            required = 28 + (form.rowCount() * 34) + ((form.rowCount() - 1) * 7)
            parent.setMinimumHeight(max(parent.minimumHeight(), required))

    for grid in root.findChildren(QGridLayout):
        grid.setHorizontalSpacing(max(grid.horizontalSpacing(), 10))
        grid.setVerticalSpacing(max(grid.verticalSpacing(), 8))


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
        table.verticalHeader().setDefaultSectionSize(34)

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
