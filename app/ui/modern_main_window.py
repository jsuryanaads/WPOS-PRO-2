from datetime import datetime

from PySide6.QtCore import Qt, QSize
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
    QSizePolicy,
    QTableWidgetItem,
)

from ..config import APP_NAME, APP_VERSION
from ..database import SessionLocal
from ..models import Product
from ..services.reports import sales_summary, low_stock_count, cash_summary, stock_summary, recent_sales
from .branding import LOGO_PATH
from .main_window import MainWindow
from .premium_cashier import apply_premium_cashier


class ModernMainWindow(MainWindow):
    """Modern POS shell around the existing WPOS PRO 2 business pages.

    This class owns structure and navigation only. Business operations remain
    in MainWindow/services; this shell only coordinates presentation state.
    """

    NAVIGATION = [
        ("OPERASIONAL", [("", "Dashboard", 0), ("", "Kasir", 1), ("", "Produk", 2), ("", "Stok & Mutasi", 3), ("", "Pembelian", 4)]),
        ("KEUANGAN", [("", "Kas", 5), ("", "Laporan", 6)]),
        ("DATA MASTER", [("", "Pelanggan", 13), ("", "Supplier", 12), ("", "Kategori", 10), ("", "Satuan", 11)]),
        ("SYSTEM", [("", "Pengaturan Toko", 7), ("", "Printer", 8), ("", "Backup / Restore", 9)]),
    ]

    PAGE_TITLES = [
        "Dashboard", "Kasir", "Produk", "Stok & Mutasi", "Pembelian", "Kas", "Laporan",
        "Pengaturan Toko", "Printer", "Backup / Restore", "Kategori", "Satuan", "Supplier", "Pelanggan",
    ]
    PAGE_HINTS = [
        "Ringkasan bisnis hari ini", "Transaksi cepat · barcode first", "Master produk & harga",
        "Kontrol persediaan", "Restock & supplier", "Arus kas toko", "Analitik & riwayat",
        "Identitas dan preferensi", "Thermal printer · 58mm", "Keamanan database lokal",
        "Kelompok produk", "Satuan barang", "Data pemasok", "Riwayat pelanggan",
    ]

    def __init__(self, user, logout_callback=None):
        super().__init__(user, logout_callback=logout_callback)
        self._build_modern_shell()
        self.showMaximized()

    def _build_modern_shell(self):
        old_tabs = self.tabs
        pages = [old_tabs.widget(i) for i in range(old_tabs.count())]
        titles = [old_tabs.tabText(i) for i in range(old_tabs.count())]
        # Do not keep a signal connection to the detached legacy QTabWidget.
        # Navigation is owned exclusively by the modern QListWidget/stack.
        old_tabs.setParent(None)
        for toolbar in self.findChildren(QWidget):
            if toolbar.__class__.__name__ == "QToolBar":
                toolbar.hide()

        shell = QWidget()
        shell.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        root = QHBoxLayout(shell)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("modernSidebar")
        sidebar.setFixedWidth(230)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(12, 12, 12, 12)
        side.setSpacing(5)

        brand = QFrame()
        brand.setObjectName("modernBrand")
        brand_l = QHBoxLayout(brand)
        brand_l.setContentsMargins(9, 8, 9, 8)
        brand_l.setSpacing(7)
        logo = QLabel()
        logo.setObjectName("modernBrandLogo")
        if LOGO_PATH.exists():
            pix = QPixmap(str(LOGO_PATH))
            if not pix.isNull():
                logo.setPixmap(pix.scaled(42, 42, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        brand_l.addWidget(logo)
        brand_text = QVBoxLayout()
        brand_text.setContentsMargins(0, 0, 0, 0)
        brand_text.setSpacing(1)
        name = QLabel(APP_NAME)
        name.setObjectName("modernBrandName")
        version = QLabel(f"{APP_VERSION} · POS 2026")
        version.setObjectName("modernBrandVersion")
        brand_text.addWidget(name)
        brand_text.addWidget(version)
        brand_l.addLayout(brand_text, 1)
        side.addWidget(brand)
        side.addSpacing(4)

        self.nav_list = QListWidget()
        self.nav_list.setObjectName("modernNav")
        self.nav_list.setSpacing(1)
        self.nav_list.setFrameShape(QFrame.NoFrame)
        self.nav_list.setFocusPolicy(Qt.NoFocus)
        self.nav_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.nav_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._nav_indexes = []
        self._nav_items = {}
        for section, entries in self.NAVIGATION:
            header = QListWidgetItem(section)
            header.setFlags(Qt.NoItemFlags)
            header.setData(Qt.UserRole, -1)
            header.setData(Qt.UserRole + 1, "section")
            header.setData(Qt.UserRole + 2, section)
            header.setSizeHint(QSize(0, 25))
            self.nav_list.addItem(header)
            for _icon, title, index in entries:
                item = QListWidgetItem(title)
                item.setData(Qt.UserRole, index)
                item.setData(Qt.UserRole + 1, "item")
                item.setSizeHint(QSize(0, 30))
                self.nav_list.addItem(item)
                self._nav_indexes.append(index)
                self._nav_items[index] = item
        self.nav_list.currentItemChanged.connect(self._navigate)
        side.addWidget(self.nav_list, 1)

        account = QFrame()
        account.setObjectName("modernAccount")
        al = QVBoxLayout(account)
        al.setContentsMargins(9, 8, 9, 8)
        al.setSpacing(2)
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
        content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_l = QVBoxLayout(content)
        content_l.setContentsMargins(22, 18, 22, 12)
        content_l.setSpacing(10)

        topbar = QFrame()
        topbar.setObjectName("modernTopbar")
        top_l = QHBoxLayout(topbar)
        top_l.setContentsMargins(16, 8, 16, 8)
        top_l.setSpacing(14)

        title_box = QVBoxLayout()
        title_box.setContentsMargins(0, 0, 0, 0)
        title_box.setSpacing(1)
        self.modern_context = QLabel("Dashboard")
        self.modern_context.setObjectName("modernContext")
        self.modern_hint = QLabel("Ringkasan bisnis hari ini")
        self.modern_hint.setObjectName("modernHint")
        title_box.addWidget(self.modern_context)
        title_box.addWidget(self.modern_hint)
        top_l.addLayout(title_box, 1)

        welcome = QLabel(f"Selamat datang, {self.user.username}")
        welcome.setObjectName("modernWelcome")
        welcome.setAlignment(Qt.AlignCenter)
        welcome.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        top_l.addWidget(welcome, 1)

        month_names = (
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember",
        )
        now = datetime.now()
        date_label = QLabel(f"{now.day} {month_names[now.month - 1]} {now.year}")
        date_label.setObjectName("modernDate")
        date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        date_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        top_l.addWidget(date_label, 0)
        content_l.addWidget(topbar)

        self.modern_stack = QStackedWidget()
        self.modern_stack.setObjectName("modernStack")
        self.modern_stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for page in pages:
            page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.modern_stack.addWidget(page)
        content_l.addWidget(self.modern_stack, 1)

        root.addWidget(sidebar, 0)
        root.addWidget(content, 1)
        self.setCentralWidget(shell)
        self.tabs = self._compat_tabs(old_tabs, titles)
        apply_premium_cashier(self)
        self._polish_dashboard()
        self._remove_cosmetic_prefixes()
        self._select_navigation(0)

    def _compat_tabs(self, old_tabs, titles):
        class CompatTabs:
            def __init__(self, owner, titles):
                self.owner = owner
                self.titles = titles
            def setCurrentIndex(self, index):
                self.owner._select_navigation(index)
            def tabText(self, index):
                if 0 <= index < len(self.titles):
                    return self.titles[index]
                return ""
            def count(self):
                return len(self.titles)
            def widget(self, index):
                if hasattr(self.owner, "modern_stack"):
                    return self.owner.modern_stack.widget(index)
                return None
        return CompatTabs(self, titles)

    def _legacy_navigation(self, index):
        # Kept only as a compatibility entry point for external legacy callers.
        self._select_navigation(index)

    def _select_navigation(self, page_index):
        if not hasattr(self, "modern_stack"):
            return
        count = self.modern_stack.count()
        if not isinstance(page_index, int) or page_index < 0 or page_index >= count:
            return
        page = self.modern_stack.widget(page_index)
        if page is None:
            return
        self.modern_stack.setCurrentIndex(page_index)
        title = page.property("modern_title") or self._title_for(page_index)
        self.modern_context.setText(title)
        self.modern_hint.setText(self._hint_for(page_index))
        item = self._nav_items.get(page_index)
        if item is not None:
            self.nav_list.blockSignals(True)
            self.nav_list.setCurrentItem(item)
            self.nav_list.blockSignals(False)
        self.on_tab_changed(page_index)

    def _navigate(self, current, _previous):
        if current is None or not hasattr(self, "modern_stack"):
            return
        index = current.data(Qt.UserRole)
        if not isinstance(index, int) or index < 0 or index >= self.modern_stack.count():
            return
        page = self.modern_stack.widget(index)
        if page is None:
            return
        self.modern_stack.setCurrentIndex(index)
        self.modern_context.setText(page.property("modern_title") or self._title_for(index))
        self.modern_hint.setText(self._hint_for(index))
        self.on_tab_changed(index)

    def refresh_dashboard_data(self):
        """Refresh dashboard KPIs and tables after transactional changes."""
        if not hasattr(self, "modern_stack") or self.modern_stack.count() == 0:
            return
        dashboard = self.modern_stack.widget(0)
        if dashboard is None:
            return
        with SessionLocal() as session:
            summary = sales_summary(session)
            low_count = low_stock_count(session)
            product_count = session.query(Product).filter_by(active=True).count()
            cash = cash_summary(session)
            recent = recent_sales(session, 8)
            low_rows = [row for row in stock_summary(session) if row["status"] != "AMAN"][:8]

        cards = dashboard.findChildren(QFrame, "card")
        values = {
            "TRANSAKSI": str(summary["transactions"]),
            "PRODUK AKTIF": str(product_count),
            "STOK MENIPIS / HABIS": str(low_count),
            "OMZET": self._money(summary["omzet"]),
            "SALDO KAS": self._money(cash["balance"]),
        }
        for card in cards:
            title = card.findChild(QLabel, "cardTitle")
            value = card.findChild(QLabel, "cardValue")
            if title is not None and value is not None and title.text() in values:
                value.setText(values[title.text()])

        table = getattr(self, "dashboard_sales", None)
        if table is not None:
            table.setRowCount(0)
            for sale in recent:
                row = table.rowCount()
                table.insertRow(row)
                data = [sale.invoice_no, sale.created_at.strftime("%d/%m/%Y %H:%M"), sale.payment_method, self._money(sale.total)]
                for column, value in enumerate(data):
                    table.setItem(row, column, QTableWidgetItem(str(value)))

        low_table = getattr(self, "dashboard_low", None)
        if low_table is not None:
            low_table.setRowCount(0)
            for item in low_rows:
                row = low_table.rowCount()
                low_table.insertRow(row)
                for column, value in enumerate([item["name"], item["stock"], item["status"]]):
                    low_table.setItem(row, column, QTableWidgetItem(str(value)))

    @staticmethod
    def _money(value):
        from decimal import Decimal
        return f"Rp {Decimal(str(value)):,.0f}".replace(",", ".")

    @classmethod
    def _title_for(cls, index):
        if 0 <= index < len(cls.PAGE_TITLES):
            return cls.PAGE_TITLES[index]
        return APP_NAME

    @classmethod
    def _hint_for(cls, index):
        if 0 <= index < len(cls.PAGE_HINTS):
            return cls.PAGE_HINTS[index]
        return "Offline POS · Local Database"

    @staticmethod
    def _shadow(widget, blur=18, y=4):
        effect = QGraphicsDropShadowEffect(widget)
        effect.setBlurRadius(blur)
        effect.setOffset(0, y)
        effect.setColor(QColor(15, 23, 42, 28))
        widget.setGraphicsEffect(effect)

    def _polish_dashboard(self):
        if not hasattr(self, "modern_stack") or self.modern_stack.count() == 0:
            return
        dashboard = self.modern_stack.widget(0)
        if dashboard is None or dashboard.layout() is None:
            return
        layout = dashboard.layout()
        if layout.count() and layout.itemAt(0).widget():
            header = layout.itemAt(0).widget()
            if header.objectName() == "":
                header.hide()
        cards = dashboard.findChildren(QFrame, "card")
        for card in cards:
            title = card.findChild(QLabel, "cardTitle")
            value = card.findChild(QLabel, "cardValue")
            if not title or not value:
                continue
            self._shadow(card, blur=16, y=3)
        for button in dashboard.findChildren(QPushButton):
            text = button.text().strip()
            if text in {"+ Transaksi Baru", "Transaksi Baru"}:
                button.setObjectName("dashboardPrimary")
            elif text in {"+ Produk", "Produk"}:
                button.setObjectName("dashboardSecondary")
            else:
                button.setObjectName("dashboardGhost")

    def _remove_cosmetic_prefixes(self):
        if not hasattr(self, "modern_stack"):
            return
        prefixes = ("+ ", "＋ ", "↻ ", "↥ ", "▣ ", "□ ", "▤ ", "◫ ", "◇ ", "⚙ ", "● ")
        for button in self.findChildren(QPushButton):
            text = button.text()
            for prefix in prefixes:
                if text.startswith(prefix):
                    button.setText(text[len(prefix):])
                    break
        for label in self.findChildren(QLabel):
            text = label.text()
            for prefix in prefixes:
                if text.startswith(prefix):
                    label.setText(text[len(prefix):])
                    break
