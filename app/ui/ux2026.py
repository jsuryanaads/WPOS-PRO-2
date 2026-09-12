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


def _normalize_numeric_inputs(window):
    """Make application numeric inputs integer-safe and prevent locale ambiguity."""
    for spin in window.findChildren(QDoubleSpinBox):
        spin.setDecimals(0)
        spin.setSingleStep(1)
        if spin.minimum() > 0:
            spin.setMinimum(1)


def apply_ux2026(window):
    """Apply theme-neutral interaction and accessibility refinements once."""
    # Clear buttons are controlled exclusively by global_ui.py.
    # Geometry and colors belong to global_ui.py and theme_shell.py.
    if getattr(window, "_wpos_ux2026_applied", False):
        return
    window.setAttribute(Qt.WA_StyledBackground, True)
    for table in window.findChildren(QTableWidget):
        table.setAlternatingRowColors(True); table.setSelectionBehavior(QAbstractItemView.SelectRows); table.setSelectionMode(QAbstractItemView.SingleSelection); table.setEditTriggers(QAbstractItemView.NoEditTriggers); table.setSortingEnabled(False); table.setFocusPolicy(Qt.StrongFocus); table.setToolTip(""); table.verticalHeader().setVisible(False); table.setWordWrap(False)
    for widget_type in (QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QTextEdit):
        for widget in window.findChildren(widget_type): widget.setFocusPolicy(Qt.StrongFocus)
    _normalize_numeric_inputs(window)
    shortcuts = []
    def focus_search():
        for edit in window.findChildren(QLineEdit):
            if edit.isVisible() and edit.isEnabled() and not edit.isReadOnly(): edit.setFocus(Qt.ShortcutFocusReason); edit.selectAll(); break
    shortcut = QShortcut(QKeySequence("Ctrl+K"), window, focus_search); shortcut.setContext(Qt.WindowShortcut); shortcuts.append(shortcut)
    for key, index in enumerate(range(10), start=1):
        nav = QShortcut(QKeySequence(f"Alt+{key}"), window, lambda i=index: window.tabs.setCurrentIndex(i)); nav.setContext(Qt.WindowShortcut); shortcuts.append(nav)
    window._wpos_ux2026_shortcuts = shortcuts; window._wpos_ux2026_applied = True
