"""Responsive, visibly modern presentation layer with realtime dashboard refresh."""

from PySide6.QtCore import QObject, QTimer, QEvent
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import QFrame, QSizePolicy, QGraphicsDropShadowEffect, QTableWidget, QListWidget


DARK_VISUAL = """
QFrame#modernSidebar { background:#111827; border-right:1px solid #253247; }
QFrame#modernBrand { background:#1b2a41; border:1px solid #304766; border-radius:16px; }
QLabel#modernBrandName { color:#f8fafc; font-size:17px; font-weight:900; }
QLabel#modernBrandVersion { color:#8ea4bf; font-size:10px; font-weight:700; }
QListWidget#modernNav { background:#111827; padding:6px 3px; }
QListWidget#modernNav::item { color:#aebdd0; min-height:36px; padding:8px 12px; margin:2px 4px; border-radius:10px; font-size:12px; }
QListWidget#modernNav::item:hover { background:#1e2a3b; color:#ffffff; }
QListWidget#modernNav::item:selected { background:#2563a8; color:#ffffff; font-weight:900; border:1px solid #3b82c4; }
QFrame#modernAccount { background:#192231; border:1px solid #2d3b4d; border-radius:14px; }
QPushButton#modernLogout { background:#253246; color:#e5edf7; border:1px solid #36475d; border-radius:10px; min-height:34px; }
QPushButton#modernLogout:hover { background:#31506f; }
QFrame#modernContent { background:#0f1722; }
QFrame#modernTopbar { background:#172231; border:1px solid #293a4f; border-radius:16px; min-height:70px; max-height:78px; }
QLabel#modernContext { color:#f8fafc; font-size:21px; font-weight:900; }
QLabel#modernHint, QLabel#modernWelcome { color:#93a4b8; }
QLabel#modernDate { color:#d6e0eb; font-size:11px; font-weight:800; }
QFrame#card { background:#172231; border:1px solid #2b3b50; border-radius:16px; min-width:170px; max-width:340px; }
QFrame#card:hover { border:1px solid #3d6e9e; }
QLabel#cardTitle { color:#8fa4bb; font-size:10px; font-weight:900; }
QLabel#cardValue { color:#f8fafc; font-size:26px; font-weight:900; }
QGroupBox { background:#172231; border:1px solid #2b3b50; border-radius:14px; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background:#111c2a; color:#eef5fc; border:1px solid #34465d; border-radius:10px; min-height:36px; padding:6px 10px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus { border:1px solid #55a8e8; }
QPushButton { background:#256fae; color:#ffffff; border:1px solid #347fbf; border-radius:10px; min-height:36px; padding:7px 15px; font-weight:800; }
QPushButton:hover { background:#3186ca; }
QPushButton:pressed { background:#1f5c91; }
QTableWidget { background:#162130; color:#e9f1f8; border:1px solid #2b3b50; border-radius:12px; alternate-background-color:#1b2939; gridline-color:#26374a; }
QTableWidget::item { padding:9px; }
QTableWidget::item:hover { background:#23364b; }
QHeaderView::section { background:#1e2e40; color:#cbd8e5; min-height:36px; padding:9px; border:0; font-weight:900; }
QFrame#premiumCashierPage, QFrame#premiumScanCard, QFrame#premiumCartCard, QFrame#premiumPayCard, QFrame#premiumChangeBox, QFrame#premiumTotalBox, QFrame#premiumTransactionControls { background:#172231; border:1px solid #2b3b50; border-radius:14px; }
QFrame#premiumScanCard { background:#1a2b3d; border-color:#36516b; }
QFrame#premiumPayCard { border-color:#3b6f9d; }
QLabel#premiumSectionTitle, QLabel#premiumControlsTitle { color:#f8fafc; font-size:14px; font-weight:900; }
QLabel#premiumMuted, QLabel#premiumFieldCaption, QLabel#premiumPayLabel, QLabel#premiumTotalCaption, QLabel#premiumChangeCaption { color:#8fa4bb; }
QLabel#premiumTotal, QLabel#premiumChange { color:#f8fafc; font-size:27px; font-weight:900; }
QPushButton#premiumCheckout { background:#159a72; border-color:#20b486; min-height:44px; font-size:13px; }
QPushButton#premiumCheckout:hover { background:#1db987; }
"""

LIGHT_VISUAL = """
QFrame#modernSidebar { background:#0f2740; border-right:1px solid #1d4163; }
QFrame#modernBrand { background:#173b60; border:1px solid #2b5b86; border-radius:16px; }
QLabel#modernBrandName { color:#ffffff; font-size:17px; font-weight:900; }
QLabel#modernBrandVersion { color:#a9c2d9; font-size:10px; font-weight:700; }
QListWidget#modernNav { background:#0f2740; padding:6px 3px; }
QListWidget#modernNav::item { color:#b7cadc; min-height:36px; padding:8px 12px; margin:2px 4px; border-radius:10px; font-size:12px; }
QListWidget#modernNav::item:hover { background:#1c4164; color:#ffffff; }
QListWidget#modernNav::item:selected { background:#2b78b8; color:#ffffff; font-weight:900; }
QFrame#modernAccount { background:#173451; border:1px solid #2b5275; border-radius:14px; }
QPushButton#modernLogout { background:#244766; color:#ffffff; border:1px solid #376184; border-radius:10px; }
QFrame#modernContent { background:#eef3f7; }
QFrame#modernTopbar { background:#ffffff; border:1px solid #d3dee7; border-radius:16px; min-height:70px; max-height:78px; }
QLabel#modernContext { color:#17324a; font-size:21px; font-weight:900; }
QLabel#modernHint, QLabel#modernWelcome { color:#708293; }
QLabel#modernDate { color:#34536d; font-size:11px; font-weight:800; }
QFrame#card { background:#ffffff; border:1px solid #d5dfe7; border-radius:16px; min-width:170px; max-width:340px; }
QFrame#card:hover { border:1px solid #7ca8c8; }
QLabel#cardTitle { color:#728494; font-size:10px; font-weight:900; }
QLabel#cardValue { color:#173b59; font-size:26px; font-weight:900; }
QGroupBox { background:#ffffff; border:1px solid #d5dfe7; border-radius:14px; }
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit { background:#ffffff; color:#253b4e; border:1px solid #cbd7e0; border-radius:10px; min-height:36px; padding:6px 10px; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus { border:1px solid #2b78b8; }
QPushButton { background:#2b78b8; color:#ffffff; border:1px solid #2b78b8; border-radius:10px; min-height:36px; padding:7px 15px; font-weight:800; }
QPushButton:hover { background:#21679f; }
QTableWidget { background:#ffffff; color:#263b4d; border:1px solid #d2dde5; border-radius:12px; alternate-background-color:#f4f7f9; gridline-color:#e1e7ec; }
QTableWidget::item { padding:9px; }
QTableWidget::item:hover { background:#eaf3f9; }
QHeaderView::section { background:#e7eef3; color:#34546d; min-height:36px; padding:9px; border:0; font-weight:900; }
QFrame#premiumCashierPage, QFrame#premiumScanCard, QFrame#premiumCartCard, QFrame#premiumPayCard, QFrame#premiumChangeBox, QFrame#premiumTotalBox, QFrame#premiumTransactionControls { background:#ffffff; border:1px solid #d5dfe7; border-radius:14px; }
QFrame#premiumScanCard { background:#edf6fc; border-color:#bcd8eb; }
QFrame#premiumPayCard { border-color:#8db6d4; }
QLabel#premiumSectionTitle, QLabel#premiumControlsTitle { color:#173b59; font-size:14px; font-weight:900; }
QLabel#premiumMuted, QLabel#premiumFieldCaption, QLabel#premiumPayLabel, QLabel#premiumTotalCaption, QLabel#premiumChangeCaption { color:#718494; }
QLabel#premiumTotal, QLabel#premiumChange { color:#173b59; font-size:27px; font-weight:900; }
QPushButton#premiumCheckout { background:#168b68; border-color:#168b68; min-height:44px; font-size:13px; }
QPushButton#premiumCheckout:hover { background:#12785a; }
"""


class _ResponsiveRealtimeController(QObject):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.timer = QTimer(self)
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self._refresh)
        self.timer.start()
        window.installEventFilter(self)
        self.apply_visuals()
        self.apply_layout()

    def eventFilter(self, watched, event):
        if watched is self.window and event.type() == QEvent.Resize:
            self.apply_layout()
        return False

    def _refresh(self):
        refresh = getattr(self.window, "refresh_dashboard_data", None)
        if callable(refresh):
            try:
                refresh()
            except Exception:
                pass

    def apply_visuals(self):
        theme = str(getattr(self.window, "_wpos_active_theme", "DARK")).upper()
        self.window.setStyleSheet(self.window.styleSheet() + (DARK_VISUAL if theme == "DARK" else LIGHT_VISUAL))
        for card in self.window.findChildren(QFrame, "card"):
            effect = QGraphicsDropShadowEffect(card)
            effect.setBlurRadius(22)
            effect.setOffset(0, 5)
            effect.setColor(QColor(0, 0, 0, 45))
            card.setGraphicsEffect(effect)
        for table in self.window.findChildren(QTableWidget):
            table.verticalHeader().setDefaultSectionSize(40)
        nav = self.window.findChild(QListWidget, "modernNav")
        if nav is not None:
            for row in range(nav.count()):
                item = nav.item(row)
                if item.data(257) == "section":
                    font = QFont("Segoe UI", 9)
                    font.setBold(True)
                    item.setFont(font)

    def apply_layout(self):
        width = self.window.width()
        sidebar = self.window.findChild(QFrame, "modernSidebar")
        if sidebar is not None:
            sidebar.setFixedWidth(178 if width < 1000 else 205 if width < 1250 else 248)
        topbar = self.window.findChild(QFrame, "modernTopbar")
        if topbar is not None:
            topbar.setMinimumHeight(64 if width < 1100 else 72)
            topbar.setMaximumHeight(72 if width < 1100 else 80)
        content = self.window.findChild(QFrame, "modernContent")
        if content is not None and content.layout() is not None:
            margin = 8 if width < 1000 else 14 if width < 1250 else 22
            content.layout().setContentsMargins(margin, 12, margin, 12)
        pay = self.window.findChild(QFrame, "premiumPayCard")
        if pay is not None:
            if width < 1000:
                pay.setMinimumWidth(230); pay.setMaximumWidth(270)
            elif width < 1250:
                pay.setMinimumWidth(260); pay.setMaximumWidth(300)
            else:
                pay.setMinimumWidth(300); pay.setMaximumWidth(360)
        stack = getattr(self.window, "modern_stack", None)
        if stack is not None:
            for index in range(stack.count()):
                page = stack.widget(index)
                if page is None:
                    continue
                page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                layout = page.layout()
                if layout is not None:
                    margin = 8 if width < 1000 else 12 if width < 1250 else 18
                    layout.setContentsMargins(margin, 8, margin, 12)


def apply_responsive_realtime(window):
    controller = getattr(window, "_wpos_responsive_realtime", None)
    if controller is None:
        controller = _ResponsiveRealtimeController(window)
        window._wpos_responsive_realtime = controller
    else:
        controller.apply_visuals()
        controller.apply_layout()
