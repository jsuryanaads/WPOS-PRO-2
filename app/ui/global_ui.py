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
    QSpinBox,
    QTableWidget,
    QTextEdit,
)


GLOBAL_UI_STYLE = """
/* WPOS PRO V2 — single UI/UX contract for every page */
QWidget {
    font-family: 'Segoe UI';
    font-size: 11px;
}

QLabel#applicationFooterLabel {
    font-size: 10px;
    font-weight: 600;
}

QLabel#pageTitle {
    font-size: 24px;
    font-weight: 900;
    color: #0f172a;
}

QLabel#pageSubtitle {
    color: #64748b;
    font-size: 11px;
}

QPushButton {
    min-height: 34px;
    border-radius: 8px;
    padding: 7px 14px;
    font-weight: 700;
}

QPushButton#primary {
    min-height: 38px;
    border-radius: 9px;
    font-weight: 800;
}

QPushButton#danger {
    background: #b91c1c;
    color: #ffffff;
}

QPushButton#danger:hover {
    background: #991b1b;
}

QLineEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox,
QTextEdit {
    min-height: 34px;
    border-radius: 8px;
    border: 1px solid #cbd5e1;
    padding: 4px 9px;
    background: #ffffff;
}

QLineEdit:focus,
QComboBox:focus,
QSpinBox:focus,
QDoubleSpinBox:focus,
QTextEdit:focus {
    border: 1px solid #2563eb;
}

QGroupBox {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px 12px 12px;
    margin-top: 12px;
    background: #ffffff;
    font-weight: 800;
    color: #334155;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 14px;
    top: 2px;
    padding: 0 7px;
    background: #ffffff;
    color: #334155;
}

QFrame#card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}

QLabel#cardTitle {
    color: #64748b;
    font-size: 10px;
    font-weight: 800;
}

QLabel#cardValue {
    color: #0f172a;
    font-size: 22px;
    font-weight: 900;
}

QLabel#total {
    background: #0f172a;
    color: #ffffff;
    border-radius: 9px;
    padding: 10px 14px;
    font-size: 18px;
    font-weight: 900;
}

QTableWidget {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    gridline-color: #eef2f7;
    alternate-background-color: #f8fafc;
    selection-background-color: #dbeafe;
    selection-color: #0f172a;
}

QTableWidget::item {
    padding: 7px;
}

QHeaderView::section {
    min-height: 32px;
    padding: 8px;
    border: 0;
    border-bottom: 1px solid #e2e8f0;
    background: #f8fafc;
    color: #475569;
    font-weight: 800;
}

QScrollBar:vertical {
    width: 9px;
    margin: 2px;
    background: transparent;
}

QScrollBar::handle:vertical {
    background: #cbd5e1;
    border-radius: 4px;
    min-height: 28px;
}

QScrollBar::handle:vertical:hover {
    background: #94a3b8;
}

QToolTip {
    background: #0f172a;
    color: #ffffff;
    border: 0;
    padding: 6px 8px;
}
"""


def apply_global_ui(app, root=None):
    """Apply one visual and interaction contract across WPOS PRO V2.

    This function deliberately changes presentation/interaction only. Existing
    page widgets, signals, database calls and business services are preserved.
    """
    app.setStyleSheet(app.styleSheet() + GLOBAL_UI_STYLE)

    if root is None:
        return

    # Give every operational page the same semantic root marker. This allows
    # future visual refinements to be made centrally instead of page-by-page.
    stack = getattr(root, "modern_stack", None)
    if stack is not None:
        for index in range(stack.count()):
            page = stack.widget(index)
            if page is not None:
                page.setObjectName(page.objectName() or f"wposPage{index}")
                page.setProperty("wpos_page_index", index)

    for table in root.findChildren(QTableWidget):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setWordWrap(False)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        table.setMinimumHeight(max(table.minimumHeight(), 180))

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

    for frame in root.findChildren(QFrame, "applicationFooter"):
        frame.setMinimumHeight(28)
        label = frame.findChild(QLabel, "applicationFooterLabel")
        if label:
            label.setAlignment(Qt.AlignCenter)
