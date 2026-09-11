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
    """Safe global UX layer for the WPOS PRO POS shell.

    Tables are read-only by default so a cashier cannot accidentally alter
    data by double-clicking. Sorting is also opt-in per page because some POS
    tables (especially the cart) have a meaningful fixed column order.
    """
    window.setAttribute(Qt.WA_StyledBackground, True)

    for table in window.findChildren(QTableWidget):
        table.setAlternatingRowColors(True)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSelectionMode(QAbstractItemView.SingleSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSortingEnabled(False)
        table.setFocusPolicy(Qt.StrongFocus)
        table.setToolTip("Klik untuk memilih · ↑ ↓ untuk berpindah")
        table.verticalHeader().setVisible(False)
        table.setWordWrap(False)

    # PySide6 does not accept a tuple of widget classes in findChildren().
    # Iterate the supported types explicitly for compatibility across Qt 6.x.
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

    window.setStyleSheet(window.styleSheet() + """
        QWidget { outline: none; }
        QToolTip {
            padding: 6px 8px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            background: #ffffff;
            color: #0f172a;
        }
        QTableWidget {
            gridline-color: #e2e8f0;
            selection-background-color: #dbeafe;
            selection-color: #0f172a;
        }
        QTableWidget::item:selected { font-weight: 700; }
        QHeaderView::section {
            min-height: 32px;
            padding: 7px 8px;
            border: 0;
            border-bottom: 1px solid #e2e8f0;
            background: #f8fafc;
            color: #475569;
            font-weight: 800;
        }
        QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox, QTextEdit {
            min-height: 34px;
            border-radius: 9px;
            border: 1px solid #cbd5e1;
            background: #ffffff;
        }
        QPushButton {
            min-height: 34px;
            border-radius: 9px;
        }
        QPushButton:focus, QLineEdit:focus, QComboBox:focus,
        QDoubleSpinBox:focus, QSpinBox:focus, QTextEdit:focus {
            border: 1px solid #2563eb;
        }
        QStatusBar {
            min-height: 26px;
            padding-left: 8px;
            padding-right: 8px;
        }

        /* Modern shell page surfaces: legacy pages must not inherit a dark
           background from the shell and must keep readable text contrast. */
        QWidget#modernStack > QWidget {
            background: #f8fafc;
            color: #0f172a;
        }
        QWidget#premiumCashierPage {
            background: #f8fafc;
            color: #0f172a;
        }
        QWidget#modernStack QWidget {
            font-size: 11px;
        }

        /* WPOS PRO V2 sidebar is a dedicated shell surface. Keep its visual
           contract isolated from theme-level QListWidget rules. */
        QFrame#modernSidebar {
            background: #0b1220;
            color: #e2e8f0;
            border: 0;
            min-width: 230px;
            max-width: 250px;
        }
        QFrame#modernBrand {
            background: #151f32;
            border: 1px solid #263550;
            border-radius: 14px;
        }
        QLabel#modernBrandName { color: #ffffff; font-size: 18px; font-weight: 900; }
        QLabel#modernBrandVersion { color: #94a3b8; font-size: 9px; font-weight: 700; }
        QListWidget#modernNav {
            background: #0b1220;
            color: #94a3b8;
            border: 0;
            outline: none;
            padding: 0;
        }
        QListWidget#modernNav::item {
            background: transparent;
            color: #94a3b8;
            padding: 9px 8px;
            margin: 1px 0;
            border: 0;
            border-radius: 8px;
            font-size: 12px;
        }
        QListWidget#modernNav::item:hover {
            background: #151f32;
            color: #ffffff;
        }
        QListWidget#modernNav::item:selected {
            background: #2563eb;
            color: #ffffff;
            font-weight: 800;
        }
        QListWidget#modernNav::item:disabled {
            background: transparent;
            color: #64748b;
            padding: 11px 8px 4px;
            margin-top: 5px;
            font-size: 9px;
            font-weight: 900;
        }
        QFrame#modernAccount {
            background: #151f32;
            border: 1px solid #263550;
            border-radius: 12px;
        }
        QLabel#modernUser { color: #ffffff; font-weight: 800; }
        QLabel#modernRole { color: #94a3b8; font-size: 10px; }
        QPushButton#modernLogout {
            background: #202d45;
            color: #e2e8f0;
            border: 1px solid #31425f;
            border-radius: 8px;
            padding: 7px;
            margin-top: 5px;
        }
        QPushButton#modernLogout:hover { background: #2b3b59; }
    """)
