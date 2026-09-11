from datetime import datetime
from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QLabel, QDoubleSpinBox, QComboBox, QTableWidget,
    QTableWidgetItem, QFormLayout, QMessageBox, QTextEdit, QFileDialog,
    QFrame, QHeaderView, QAbstractItemView, QGroupBox, QSpinBox, QToolBar
)

from ..config import APP_NAME
from ..database import SessionLocal, engine
from ..models import Product, Supplier, Category, Unit, Sale
from ..services.sales import create_sale
from ..services.products import create_product, update_product, deactivate_product
from ..services.stock import adjust_stock
from ..services.purchases import create_purchase
from ..services.cash import record_cash_movement
from ..services.reports import sales_summary, low_stock_count, cash_summary, stock_summary, recent_sales
from ..services.backup import backup_database, restore_database
from ..services.settings import get_settings, save_settings
from ..services.printer import available_printers, print_receipt, test_print
from .master_data import category_page, unit_page, supplier_page, customer_page


def money(value):
    return f"Rp {Decimal(str(value)):,.0f}".replace(",", ".")


class MainWindow(QMainWindow):
    def __init__(self, user, logout_callback=None):
        super().__init__()
        self.user = user
        self.logout_callback = logout_callback
        self.cart = []
        self.selected_product_id = None
        self.setWindowTitle(APP_NAME)
        self.resize(1280, 800)
        self.setMinimumSize(1050, 680)
        # Theme styling is centralized in themes.py/theme_shell.py/global_ui.py.
        # Do not install a widget-local legacy stylesheet here: local QSS would
        # override the active application theme and make pages visually diverge.

        account_toolbar = QToolBar("Akun")
        account_toolbar.setMovable(False)
        account_toolbar.setFloatable(False)
        account_toolbar.setToolButtonStyle(Qt.ToolButtonTextOnly)
        self.addToolBar(Qt.TopToolBarArea, account_toolbar)
        account_toolbar.addWidget(QLabel(f"  {self.user.username} · {self.user.role}  "))
        account_toolbar.addSeparator()
        logout = QPushButton("Keluar")
        logout.setObjectName("danger")
        logout.setMinimumHeight(32)
        logout.setToolTip("Keluar dari akun dan kembali ke halaman login")
        logout.clicked.connect(self.logout)
        account_toolbar.addWidget(logout)

        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setMovable(False)
        self.tabs = tabs
        pages = [
            (self.dashboard(), "Dashboard"), (self.cashier(), "Kasir"), (self.products(), "Produk"),
            (self.stock_page(), "Stok & Mutasi"), (self.purchase_page(), "Pembelian"), (self.cash_page(), "Kas"),
            (self.report_page(), "Laporan"), (self.settings_page(), "Pengaturan Toko"), (self.printer_page(), "Printer"),
            (self.backup_page(), "Backup / Restore"), (category_page(), "Kategori"), (unit_page(), "Satuan"),
            (supplier_page(), "Supplier"), (customer_page(), "Pelanggan"),
        ]
        for widget, title in pages:
            tabs.addTab(widget, title)
        tabs.currentChanged.connect(self.on_tab_changed)
        self.setCentralWidget(tabs)

    def logout(self):
        answer = QMessageBox.question(
            self,
            "Keluar",
            f"Yakin ingin keluar dari akun {self.user.username}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return
        self.cart.clear()
        if self.logout_callback:
            self.logout_callback(self)
        else:
            self.close()

    def _stylesheet(self):
        """Legacy compatibility hook; active themes now own all presentation."""
        return ""

    def page_header(self, title, subtitle):
        box = QWidget(); layout = QVBoxLayout(box); layout.setContentsMargins(0, 0, 0, 8)
        t = QLabel(title); t.setObjectName("pageTitle"); s = QLabel(subtitle); s.setObjectName("pageSubtitle")
        layout.addWidget(t); layout.addWidget(s); return box

    def card(self, title, value):
        frame = QFrame(); frame.setObjectName("card"); layout = QVBoxLayout(frame); layout.setContentsMargins(16, 14, 16, 14)
        a = QLabel(title); a.setObjectName("cardTitle"); b = QLabel(value); b.setObjectName("cardValue"); layout.addWidget(a); layout.addWidget(b); return frame, b

    def dashboard(self):
        w = QWidget(); l = QVBoxLayout(w); l.setContentsMargins(18, 16, 18, 18)
        l.addWidget(self.page_header("Dashboard", f"Selamat datang, {self.user.username} · Role {self.user.role}"))
        with SessionLocal() as s:
            summary = sales_summary(s); low = low_stock_count(s); products = s.query(Product).filter_by(active=True).count(); cash = cash_summary(s); recent = recent_sales(s, 8); low_rows = [x for x in stock_summary(s) if x["status"] != "AMAN"][:8]
        grid = QGridLayout(); grid.setSpacing(12)
        for i, (frame, _) in enumerate([self.card("TRANSAKSI", str(summary["transactions"])), self.card("PRODUK AKTIF", str(products)), self.card("STOK MENIPIS / HABIS", str(low)), self.card("OMZET", money(summary["omzet"])), self.card("SALDO KAS", money(cash["balance"]))]): grid.addWidget(frame, 0, i)
        l.addLayout(grid); actions = QHBoxLayout()