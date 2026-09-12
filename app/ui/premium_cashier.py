from PySide6.QtCore import QObject
from PySide6.QtGui import QKeySequence, QShortcut

# ...

def _install_shortcuts(window):
    if getattr(window, "_wpos_cashier_shortcuts_installed", False):
        return
    shortcuts = []
    parent = window if isinstance(window, QObject) else getattr(window, "modern_stack", None)
    if parent is None:
        return
    for key, callback in [("F4", window.checkout), ("Escape", lambda: _cancel(window)), ("F8", lambda: _history(window)), ("F9", lambda: _show_held(window)), ("F10", lambda: _hold_current(window))]:
        shortcut = QShortcut(QKeySequence(key), parent, callback)
        shortcuts.append(shortcut)
    window._cashier_shortcuts = shortcuts
    window._wpos_cashier_shortcuts_installed = True
