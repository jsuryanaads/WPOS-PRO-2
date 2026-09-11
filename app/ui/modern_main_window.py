from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ..config import APP_VERSION
from .branding import LOGO_PATH
from .main_window import MainWindow
from .premium_cashier import apply_premium_cashier


class ModernMainWindow(MainWindow):
    """Modern POS 2026 shell around the existing WPOS PRO business pages."""

    NAVIGATION = [
        ("OPERASIONAL", [("▣", "Dashboard", 0), ("＋", "Kasir", 1), ("□", "Produk", 2), ("▤", "Stok & Mutasi", 3), ("↥", "Pembelian", 4)]),
        ("KEUANGAN", [("Rp", "Kas", 5), ("◫", "Laporan", 6)]),
        ("DATA MASTER", [("◎", "Pelanggan", 13), ("◉", "Supplier", 12), ("◇", "Kategori", 10), ("◇", "Satuan", 11)]),
        ("SISTEM", [("⚙", "Pengaturan Toko", 7), ("▣", "Printer", 8), ("↻", "Backup / Restore", 9)]),
    ]

    def __init__(self, user, logout_callback=None):
        super().__init__(user, logout_callback=logout_callback)
        self._build_modern_shell()

    def _build_modern_shell(self):
        old_tabs = self.tabs
        pages = [old_tabs.widget(i) for i in range(old_tabs.count())]
        titles = [old_tabs.tabText(i) for i in range(old_tabs.count())]
        old_tabs.currentChanged.connect(self._legacy_navigation)
        old_tabs.setParent(None)
        for toolbar in self.findChildren(QWidget):
            if toolbar.__class__.__name__ == "QToolBar":
                toolbar.hide()

        shell = QWidget()
        root = QHBoxLayout(shell)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("modernSidebar")
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(14, 16, 14, 14)
        side.setSpacing(6)

        brand = QFrame()
        brand.setObjectName("modernBrand")
        brand_l = QHBoxLayout(brand)
        brand_l.setContentsMargins(10, 10, 10, 10)
        logo = QLabel()
        logo.setObjectName("modernBrandLogo")
        if LOGO_PATH.exists():
            pix = QPixmap(str(LOGO_PATH))
            if not pix.isNull():
                logo.setPixmap(pix.scaled(44, 44, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        brand_l.addWidget(logo)
        brand_text = QVBoxLayout()
        brand_text.setContentsMargins(0, 0, 0, 0)
        brand_text.setSpacing(1)
        name = QLabel("WPOS PRO")
        name.setObjectName("modernBrandName")
        version = QLabel(f"{APP_VERSION} · POS 2026")
        version.setObjectName("modernBrandVersion")
        brand_text.addWidget(name)
        brand_text.addWidget(version)
        brand_l.addLayout(brand_text, 1)
        side.addWidget(brand)
        side.addSpacing(8)

        self.nav_list = QListWidget()
        self.nav_list.setObjectName("modernNav")
        self.nav_list.setSpacing(2)
        self.nav_list.setFrameShape(QFrame.NoFrame)
        self.nav_list.setFocusPolicy(Qt.NoFocus)
        self._nav_indexes = []
        for section, entries in self.NAVIGATION:
            header = QListWidgetItem(section)
            header.setFlags(Qt.NoItemFlags)
            header.setData(Qt.UserRole, -1)
            self.nav_list.addItem(header)
            for icon, title, index in entries:
                item = QListWidgetItem(f"  {icon}   {title}")
                item.setData(Qt.UserRole, index)
                item.setToolTip(title)
                self.nav_list.addItem(item)
                self._nav_indexes.append(index)
        self.nav_list.currentItemChanged.connect(self._navigate)
        side.addWidget(self.nav_list, 1)

        account = QFrame()
        account.setObjectName("modernAccount")
        al = QVBoxLayout(account)
        al.setContentsMargins(10, 9, 10, 9)
        al.setSpacing(3)
        user_label = QLabel(f"{self.user.username}")
        user_label.setObjectName("modernUser")
        role_label = QLabel(f"{self.user.role} · Lokal")
        role_label.setObjectName("modernRole")
        al.addWidget(user_label)
        al.addWidget(role_label)
        logout = QPushButton("Keluar")
        logout.setObjectName("modernLogout")
        logout.clicked.connect(self.logout)
        al.addWidget(logout)
        side.addWidget(account)

        content = QFrame()
        content.setObjectName("modernContent")
        content_l = QVBoxLayout(content)
        content_l.setContentsMargins(22, 18, 22, 12)
        content_l.setSpacing(10)

        topbar = QFrame()
        topbar.setObjectName("modernTopbar")
        top_l = QHBoxLayout(topbar)
        top_l.setContentsMargins(16, 10, 16, 10)
        top_l.setSpacing(12)
        title_box = QVBoxLayout()
        title_box.setContentsMargins(0, 0, 0, 0)
        title_box.setSpacing(2)
        self.modern_context = QLabel("Dashboard")
        self.modern_context.setObjectName("modernContext")
        self.modern_hint = QLabel("Ringkasan bisnis hari ini")
        self.modern_hint.setObjectName("modernHint")
        title_box.addWidget(self.modern_context)
        title_box.addWidget(self.modern_hint)
        top_l.addLayout(title_box, 1)
        offline = QLabel("● OFFLINE")
        offline.setObjectName("modernStatusOffline")
        local = QLabel("DATABASE LOKAL")
        local.setObjectName("modernStatusLocal")
        top_l.addWidget(offline)
        top_l.addWidget(local)
        content_l.addWidget(topbar)

        self.modern_stack = QStackedWidget()
        self.modern_stack.setObjectName("modernStack")
        for page in pages:
            self.modern_stack.addWidget(page)
        content_l.addWidget(self.modern_stack, 1)

        root.addWidget(sidebar, 0)
        root.addWidget(content, 1)
        self.setCentralWidget(shell)
        self.tabs = self._compat_tabs(old_tabs, titles)
        apply_premium_cashier(self)
        self._select_navigation(0)
        self._apply_modern_style()
        self._polish_dashboard()

    def _compat_tabs(self, old_tabs, titles):
        class CompatTabs:
            def __init__(self, owner, titles):
                self.owner = owner
                self.titles = titles
            def setCurrentIndex(self, index):
                self.owner._select_navigation(index)
            def tabText(self, index):
                return self.titles[index]
        return CompatTabs(self, titles)

    def _legacy_navigation(self, index):
        if index >= 0 and hasattr(self, "modern_stack"):
            self._select_navigation(index)

    def _select_navigation(self, page_index):
        self.modern_stack.setCurrentIndex(page_index)
        title = self.modern_stack.widget(page_index).property("modern_title") or self._title_for(page_index)
        self.modern_context.setText(title)
        self.modern_hint.setText(self._hint_for(page_index))
        for row in range(self.nav_list.count()):
            item = self.nav_list.item(row)
            if item.data(Qt.UserRole) == page_index:
                self.nav_list.blockSignals(True)
                self.nav_list.setCurrentItem(item)
                self.nav_list.blockSignals(False)
                break
        self.on_tab_changed(page_index)

    def _navigate(self, current, _previous):
        if current is None:
            return
        index = current.data(Qt.UserRole)
        if isinstance(index, int) and index >= 0:
            self.modern_stack.setCurrentIndex(index)
            self.modern_context.setText(self._title_for(index))
            self.modern_hint.setText(self._hint_for(index))
            self.on_tab_changed(index)

    @staticmethod
    def _title_for(index):
        return [
            "Dashboard", "Kasir", "Produk", "Stok & Mutasi", "Pembelian", "Kas", "Laporan",
            "Pengaturan Toko", "Printer", "Backup / Restore", "Kategori", "Satuan", "Supplier", "Pelanggan",
        ][index]

    @staticmethod
    def _hint_for(index):
        return [
            "Ringkasan bisnis hari ini", "Transaksi cepat · barcode first", "Master produk & harga",
            "Kontrol persediaan", "Restock & supplier", "Arus kas toko", "Analitik & riwayat",
            "Identitas dan preferensi", "Thermal printer · 58mm", "Keamanan database lokal",
            "Kelompok produk", "Satuan barang", "Data pemasok", "Riwayat pelanggan",
        ][index]

    @staticmethod
    def _shadow(widget, blur=18, y=4):
        effect = QGraphicsDropShadowEffect(widget)
        effect.setBlurRadius(blur)
        effect.setOffset(0, y)
        effect.setColor(QColor(15, 23, 42, 28))
        widget.setGraphicsEffect(effect)

    def _polish_dashboard(self):
        """Apply the clean dashboard hierarchy without changing business logic."""
        dashboard = self.modern_stack.widget(0)
        if dashboard is None or dashboard.layout() is None:
            return

        layout = dashboard.layout()
        if layout.count() and layout.itemAt(0).widget():
            header = layout.itemAt(0).widget()
            if header.objectName() == "":
                header.hide()

        cards = dashboard.findChildren(QFrame, "card")
        icons = {
            "TRANSAKSI": "↗",
            "PRODUK AKTIF": "▦",
            "STOK MENIPIS / HABIS": "⚠",
            "OMZET": "Rp",
            "SALDO KAS": "▣",
        }
        for card in cards:
            title = card.findChild(QLabel, "cardTitle")
            value = card.findChild(QLabel, "cardValue")
            if not title or not value:
                continue
            title_text = title.text()
            if title_text in icons and not card.findChild(QLabel, "dashboardMetricIcon"):
                card_layout = card.layout()
                card_layout.takeAt(0)
                card_layout.takeAt(0)
                row = QHBoxLayout()
                row.setContentsMargins(0, 0, 0, 0)
                row.setSpacing(8)
                row.addWidget(title)
                row.addStretch()
                icon = QLabel(icons[title_text])
                icon.setObjectName("dashboardMetricIcon")
                row.addWidget(icon)
                card_layout.insertLayout(0, row)
                card_layout.addWidget(value)
            self._shadow(card, blur=16, y=3)

        for button in dashboard.findChildren(QPushButton):
            text = button.text().strip()
            if text == "+ Transaksi Baru":
                button.setObjectName("dashboardPrimary")
            elif text == "+ Produk":
                button.setObjectName("dashboardSecondary")
            else:
                button.setObjectName("dashboardGhost")

    def _apply_modern_style(self):
        self.setStyleSheet(self.styleSheet() + """
        QFrame#modernSidebar { background: #0b1220; border: 0; min-width: 230px; max-width: 250px; }
        QFrame#modernBrand { background: #151f32; border: 1px solid #263550; border-radius: 14px; }
        QLabel#modernBrandLogo { min-width: 44px; max-width: 44px; min-height: 44px; max-height: 44px; }
        QLabel#modernBrandName { color: #ffffff; font-size: 18px; font-weight: 900; }
        QLabel#modernBrandVersion { color: #94a3b8; font-size: 9px; font-weight: 700; }
        QListWidget#modernNav { background: transparent; color: #94a3b8; border: 0; }
        QListWidget#modernNav::item { padding: 9px 8px; border-radius: 8px; margin: 1px 0; font-size: 12px; }
        QListWidget#modernNav::item:hover { background: #151f32; color: #ffffff; }
        QListWidget#modernNav::item:selected { background: #2563eb; color: #ffffff; font-weight: 800; }
        QListWidget#modernNav::item:disabled { color: #64748b; padding: 11px 8px 4px; font-size: 9px; font-weight: 900; }
        QFrame#modernAccount { background: #151f32; border: 1px solid #263550; border-radius: 12px; }
        QLabel#modernUser { color: #ffffff; font-weight: 800; }
        QLabel#modernRole { color: #94a3b8; font-size: 10px; }
        QPushButton#modernLogout { background: #202d45; color: #e2e8f0; border: 1px solid #31425f; border-radius: 8px; padding: 7px; margin-top: 5px; }
        QPushButton#modernLogout:hover { background: #2b3b59; }
        QFrame#modernContent { background: #f8fafc; }
        QFrame#modernTopbar { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; }
        QLabel#modernContext { color: #0f172a; font-size: 17px; font-weight: 900; }
        QLabel#modernHint { color: #64748b; font-size: 10px; }
        QLabel#modernStatusOffline { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; border-radius: 999px; padding: 5px 9px; font-size: 9px; font-weight: 900; }
        QLabel#modernStatusLocal { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; border-radius: 999px; padding: 5px 9px; font-size: 9px; font-weight: 900; }
        QStackedWidget#modernStack { background: transparent; border: 0; }

        QWidget#modernStack QWidget { font-size: 11px; }
        QGroupBox { margin-top: 12px; padding: 16px 12px 12px; border-radius: 12px; border: 1px solid #e2e8f0; background: #ffffff; font-weight: 800; }
        QGroupBox::title { subcontrol-origin: margin; left: 14px; top: 2px; padding: 0 7px; color: #334155; background: #ffffff; }
        QLineEdit, QDoubleSpinBox, QComboBox, QTextEdit, QSpinBox { min-height: 34px; border-radius: 8px; border: 1px solid #cbd5e1; padding: 4px 9px; background: #ffffff; }
        QLineEdit:focus, QDoubleSpinBox:focus, QComboBox:focus, QTextEdit:focus, QSpinBox:focus { border: 1px solid #2563eb; }
        QPushButton { min-height: 34px; border-radius: 8px; padding: 7px 14px; font-weight: 700; }
        QPushButton:hover { background: #eff6ff; }
        QPushButton:pressed { padding-top: 8px; }
        QTableWidget { border-radius: 10px; border: 1px solid #e2e8f0; background: #ffffff; gridline-color: #eef2f7; alternate-background-color: #f8fafc; selection-background-color: #dbeafe; selection-color: #0f172a; }
        QTableWidget::item { padding: 7px; }
        QHeaderView::section { padding: 9px 8px; border: 0; border-bottom: 1px solid #e2e8f0; background: #f8fafc; color: #475569; font-weight: 800; }
        QScrollBar:vertical { width: 9px; margin: 2px; background: transparent; }
        QScrollBar::handle:vertical { min-height: 30px; border-radius: 4px; background: #cbd5e1; }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
        QLabel#pageTitle { font-size: 24px; font-weight: 900; color: #0f172a; }
        QLabel#pageSubtitle { color: #64748b; font-size: 11px; }
        QFrame#card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px; }
        QLabel#cardTitle { color: #64748b; font-size: 10px; font-weight: 800; }
        QLabel#cardValue { color: #0f172a; font-size: 22px; font-weight: 900; }
        QLabel#dashboardMetricIcon { min-width: 28px; max-width: 28px; min-height: 28px; max-height: 28px; padding: 3px; border-radius: 8px; background: #eff6ff; color: #2563eb; font-size: 12px; font-weight: 900; qproperty-alignment: AlignCenter; }
        QLabel#total { color: #1d4ed8; font-size: 22px; font-weight: 900; }
        QPushButton#primary { background: #2563eb; color: #ffffff; border: 0; min-height: 40px; font-weight: 900; }
        QPushButton#primary:hover { background: #1d4ed8; }
        QPushButton#danger { background: #fee2e2; color: #b91c1c; border: 0; }
        QPushButton#dashboardPrimary { background: #2563eb; color: #ffffff; border: 0; min-height: 38px; border-radius: 9px; font-weight: 900; }
        QPushButton#dashboardPrimary:hover { background: #1d4ed8; }
        QPushButton#dashboardSecondary { background: #0f766e; color: #ffffff; border: 0; min-height: 38px; border-radius: 9px; font-weight: 900; }
        QPushButton#dashboardSecondary:hover { background: #0d9488; }
        QPushButton#dashboardGhost { background: #ffffff; color: #334155; border: 1px solid #dbe3ec; min-height: 38px; border-radius: 9px; }
        QPushButton#dashboardGhost:hover { background: #eff6ff; color: #1d4ed8; border-color: #bfdbfe; }

        /* Premium POS cashier */
        QLabel#premiumPageTitle { color: #0f172a; font-size: 24px; font-weight: 950; }
        QLabel#premiumPageSubtitle { color: #64748b; font-size: 11px; }
        QLabel#premiumShortcut { color: #64748b; font-size: 9px; font-weight: 700; }
        QFrame#premiumScanCard { background: #0f172a; border: 1px solid #1e293b; border-radius: 14px; }
        QLabel#premiumFieldCaption { color: #94a3b8; font-size: 9px; font-weight: 900; letter-spacing: 1px; }
        QLineEdit#premiumBarcode { min-height: 46px; border: 2px solid #334155; border-radius: 10px; background: #ffffff; color: #0f172a; font-size: 15px; font-weight: 700; padding: 5px 13px; }
        QLineEdit#premiumBarcode:focus { border: 2px solid #3b82f6; }
        QDoubleSpinBox#premiumQty { min-height: 46px; min-width: 88px; border-radius: 10px; background: #ffffff; font-size: 13px; font-weight: 800; }
        QPushButton#premiumAdd { min-height: 46px; border-radius: 10px; background: #2563eb; color: #ffffff; padding: 0 18px; font-weight: 900; }
        QPushButton#premiumAdd:hover { background: #3b82f6; }
        QFrame#premiumCartCard, QFrame#premiumPayCard { background: #ffffff; border: 1px solid #dfe6ef; border-radius: 14px; }
        QLabel#premiumSectionTitle { color: #0f172a; font-size: 13px; font-weight: 900; }
        QLabel#premiumMuted { color: #94a3b8; font-size: 8px; font-weight: 800; }
        QTableWidget#premiumCartTable { border: 0; border-top: 1px solid #e8edf4; border-radius: 0; gridline-color: #f0f3f7; }
        QTableWidget#premiumCartTable QHeaderView::section { background: #ffffff; color: #64748b; padding: 10px 8px; border-bottom: 1px solid #e8edf4; font-size: 9px; }
        QFrame#premiumTotalBox { background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 12px; }
        QLabel#premiumTotalCaption { color: #2563eb; font-size: 9px; font-weight: 900; }
        QLabel#premiumTotal { color: #1d4ed8; font-size: 29px; font-weight: 950; }
        QLabel#premiumPayLabel { color: #475569; font-size: 10px; font-weight: 800; min-width: 45px; }
        QDoubleSpinBox#premiumMoneyInput, QComboBox#premiumMethod { min-height: 38px; border-radius: 9px; font-weight: 800; }
        QFrame#premiumChangeBox { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; }
        QLabel#premiumChangeCaption { color: #64748b; font-size: 8px; font-weight: 900; }
        QLabel#premiumChange { color: #0f766e; font-size: 20px; font-weight: 950; }
        QPushButton#premiumCheckout { background: #0f766e; color: #ffffff; border: 0; border-radius: 10px; font-size: 12px; font-weight: 950; }
        QPushButton#premiumCheckout:hover { background: #0d9488; }
        QPushButton#premiumClear { background: #f1f5f9; color: #475569; border: 1px solid #dbe3ec; border-radius: 10px; }
        QPushButton#premiumClear:hover { background: #e2e8f0; }
        """)
        self.setWindowTitle(f"WPOS PRO {APP_VERSION}")
        self.setMinimumSize(1180, 720)
