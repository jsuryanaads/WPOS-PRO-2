from PySide6.QtCore import Qt, QTimer
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


def _compact_numeric_display(spin):
    """Keep numeric values unchanged while removing misleading .000 display."""
    def compact():
        value = spin.value()
        decimals = spin.decimals()
        text = f"{value:.{decimals}f}".rstrip("0").rstrip(".")
        if not text:
            text = "0"
        text = text.replace(".", spin.locale().decimalPoint())
        spin.lineEdit().setText(text)

    def schedule_compact(_value=None):
        QTimer.singleShot(0, compact)

    spin.valueChanged.connect(schedule_compact)
    spin.editingFinished.connect(compact)
    QTimer.singleShot(0, compact)


def apply_ux2026(window):
    """Apply theme-neutral interaction and accessibility refinements.

    Geometry and colors belong to global_ui.py and theme_shell.py. This layer
    intentionally contains no palette or color rules so it cannot override
    the active WPOS PRO 2 theme.

    Global control policy also belongs to global_ui.py. In particular this
    layer must never re-enable native QLineEdit clear buttons, because that
    would override the application-wide text-first input contract.
    """
    window.setAttribute(Qt.WA_StyledBackground, True)

    for table in window.findChildren(QTableWidget):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSortingEnabled(False)
        table.setFocusPolicy(Qt.StrongFocus)
        table.setToolTip("")
        table.verticalHeader().setVisible(False)
        table.setWordWrap(False)

    for widget_type in (QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QTextEdit):
        for widget in window.findChildren(widget_type):
            widget.setFocusPolicy(Qt.StrongFocus)
            # Clear buttons are controlled exclusively by global_ui.py.
            # Never enable them here.

    # QDoubleSpinBox keeps up to three decimal places for genuine fractional
    # quantities, but the visible value is compacted: 1 -> 1, 1.2 -> 1.2,
    # 1000 -> 1000. This is presentation-only; the stored numeric value is
    # never multiplied or converted to thousands.
    for spin in window.findChildren(QDoubleSpinBox):
        _compact_numeric_display(spin)

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
