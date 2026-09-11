from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QSpinBox,
    QTableWidget,
    QTextEdit,
)


def apply_ux2026(window):
    """Apply theme-neutral interaction and accessibility refinements.

    Geometry and colors belong to global_ui.py and theme_shell.py. This layer
    intentionally contains no palette or color rules so it cannot override
    the active WPOS PRO 2 theme.
    """
    window.setAttribute(Qt.WA_StyledBackground, True)

    for table in window.findChildren(QTableWidget):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSortingEnabled(False)
        table.setFocusPolicy(Qt.StrongFocus)
        # Keep keyboard navigation available without displaying a persistent
        # instructional tooltip over the dashboard/table workspace.
        table.setToolTip("")
        table.verticalHeader().setVisible(False)
        table.setWordWrap(False)

    for widget_type in (QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QTextEdit):
        for widget in window.findChildren(widget_type):
            widget.setFocusPolicy(Qt.StrongFocus)
            if isinstance(widget, QLineEdit):
                widget.setClearButtonEnabled(True)

    shortcut = QShortcut(QKeySequence("Ctrl+K"), window)
    shortcut.setContext(Qt.WindowShortcut)

    def focus_search():
        for edit in window.findChildren(QLineEdit):
            if edit.isVisible() and edit.isEnabled() and not edit.isReadOnly():
                edit.setFocus(Qt.ShortcutFocusReason)
                edit.selectAll()
                break

    shortcut.activated.connect(focus_search)

    for key, index in enumerate(range(10), start=1):
        nav = QShortcut(QKeySequence(f"Alt+{key}"), window)
        nav.setContext(Qt.WindowShortcut)
        nav.activated.connect(lambda i=index: window.tabs.setCurrentIndex(i))
