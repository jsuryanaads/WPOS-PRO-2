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
/* WPOS PRO V2 — single UI/UX contract */
QWidget { font-family: 'Segoe UI'; }
QLabel#applicationFooterLabel { font-size: 10px; font-weight: 600; }
QPushButton { min-height: 34px; border-radius: 9px; padding: 7px 14px; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
    min-height: 34px;
    border-radius: 9px;
}
QTableWidget {
    border-radius: 9px;
    selection-background-color: palette(highlight);
    selection-color: palette(highlighted-text);
}
QHeaderView::section { min-height: 32px; padding: 7px 8px; font-weight: 800; }
QGroupBox { border-radius: 10px; padding: 12px 8px 8px; }
"""


def apply_global_ui(app, root=None):
    """Apply the single geometry/interaction contract to the whole application.

    Theme colors remain owned by themes.py; this layer owns consistent sizing,
    typography and interaction behavior so every page looks and behaves alike.
    """
    app.setStyleSheet(app.styleSheet() + GLOBAL_UI_STYLE)

    if root is None:
        return

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

    for group in root.findChildren(QGroupBox):
        group.setContentsMargins(8, 12, 8, 8)

    for frame in root.findChildren(QFrame, "applicationFooter"):
        frame.setMinimumHeight(28)
        label = frame.findChild(QLabel, "applicationFooterLabel")
        if label:
            label.setAlignment(Qt.AlignCenter)
