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
        self.setWindowTitle("WPOS PRO V1.0")
        self.resize(1280, 800)
        self.setMinimumSize(1050, 680)
        self.setStyleSheet(self._stylesheet())

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
        return """
        QMainWindow { background: #f4f6f8; } QTabWidget::pane { border: 0; background: #f4f6f8; }
        QTabBar::tab { padding: 9px 15px; margin-right: 2px; background: #e8ebef; border: 0; }
        QTabBar::tab:selected { background: #ffffff; font-weight: 700; }
        QLabel#pageTitle { font-size: 24px; font-weight: 800; color: #17202a; } QLabel#pageSubtitle { color: #667085; font-size: 13px; }
        QFrame#card { background: white; border: 1px solid #e2e6ea; border-radius: 10px; } QLabel#cardTitle { color: #667085; font-size: 12px; font-weight: 600; }
        QLabel#cardValue { color: #111827; font-size: 22px; font-weight: 800; } QGroupBox { background: white; border: 1px solid #e2e6ea; border-radius: 10px; margin-top: 10px; padding-top: 12px; font-weight: 700; }
        QGroupBox::title { subcontrol-origin: margin; left: 12px; padding: 0 5px; } QLineEdit, QDoubleSpinBox, QComboBox, QTextEdit { background: white; border: 1px solid #cfd5dc; border-radius: 6px; padding: 6px; }
        QPushButton { background: #1f2937; color: white; border: 0; border-radius: 6px; padding: 8px 14px; font-weight: 700; } QPushButton:hover { background: #374151; }
        QPushButton#primary { background: #111827; font-size: 14px; padding: 10px 18px; } QPushButton#danger { background: #b42318; }
        QLabel#total { background: #111827; color: white; border-radius: 8px; padding: 10px 14px; font-size: 18px; font-weight: 800; }
        QTableWidget { background: white; border: 1px solid #e2e6ea; border-radius: 8px; gridline-color: #eef0f2; } QHeaderView::section { background: #f3f4f6; padding: 7px; border: 0; font-weight: 700; }
        """

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
        for text, index in [("+ Transaksi Baru", 1), ("+ Produk", 2), ("Stok & Mutasi", 3), ("Laporan", 6)]:
            b = QPushButton(text); b.clicked.connect(lambda checked=False, idx=index: self.tabs.setCurrentIndex(idx)); actions.addWidget(b)
        actions.addStretch(); l.addLayout(actions)
        body = QHBoxLayout(); recent_box = QGroupBox("Transaksi Terakhir"); recent_layout = QVBoxLayout(recent_box); self.dashboard_sales = QTableWidget(0, 4); self.dashboard_sales.setHorizontalHeaderLabels(["Invoice", "Waktu", "Metode", "Total"]); self._prepare_table(self.dashboard_sales); recent_layout.addWidget(self.dashboard_sales)
        for sale in recent:
            row = self.dashboard_sales.rowCount(); self.dashboard_sales.insertRow(row)
            for c, v in enumerate([sale.invoice_no, sale.created_at.strftime("%d/%m/%Y %H:%M"), sale.payment_method, money(sale.total)]): self.dashboard_sales.setItem(row, c, QTableWidgetItem(str(v)))
        low_box = QGroupBox("Perhatian Stok"); low_layout = QVBoxLayout(low_box); self.dashboard_low = QTableWidget(0, 3); self.dashboard_low.setHorizontalHeaderLabels(["Produk", "Stok", "Status"]); self._prepare_table(self.dashboard_low); low_layout.addWidget(self.dashboard_low)
        for item in low_rows:
            row = self.dashboard_low.rowCount(); self.dashboard_low.insertRow(row)
            for c, v in enumerate([item["name"], item["stock"], item["status"]]): self.dashboard_low.setItem(row, c, QTableWidgetItem(str(v)))
        body.addWidget(recent_box, 3); body.addWidget(low_box, 2); l.addLayout(body, 1); return w

    def _prepare_table(self, table):
        table.setSelectionBehavior(QAbstractItemView.SelectRows); table.setEditTriggers(QAbstractItemView.NoEditTriggers); table.setAlternatingRowColors(True); table.horizontalHeader().setStretchLastSection(True); table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch); table.verticalHeader().setVisible(False)

    def cashier(self):
        w = QWidget(); l = QVBoxLayout(w); l.setContentsMargins(18, 16, 18, 18); l.addWidget(self.page_header("Kasir", "Scan barcode, susun keranjang, lalu selesaikan pembayaran."))
        scan = QGroupBox("Input Barang"); scan_l = QHBoxLayout(scan); self.barcode = QLineEdit(); self.barcode.setPlaceholderText("Scan / ketik barcode lalu Enter"); self.barcode.returnPressed.connect(self.add_barcode); self.qty = QDoubleSpinBox(); self.qty.setRange(0.001, 999999); self.qty.setDecimals(3); self.qty.setValue(1); add = QPushButton("Tambah Barang"); add.setObjectName("primary"); add.clicked.connect(self.add_barcode); scan_l.addWidget(QLabel("Barcode")); scan_l.addWidget(self.barcode, 3); scan_l.addWidget(QLabel("Qty")); scan_l.addWidget(self.qty); scan_l.addWidget(add); l.addWidget(scan)
        self.cart_table = QTableWidget(0, 5); self.cart_table.setHorizontalHeaderLabels(["Barcode", "Produk", "Qty", "Harga", "Subtotal"]); self._prepare_table(self.cart_table); l.addWidget(self.cart_table, 1)
        pay = QGroupBox("Pembayaran"); pay_l = QGridLayout(pay); self.discount = QDoubleSpinBox(); self.discount.setRange(0, 999999999); self.discount.valueChanged.connect(self.refresh_cart); self.paid = QDoubleSpinBox(); self.paid.setRange(0, 999999999); self.method = QComboBox(); self.method.addItems(["CASH", "QRIS", "TRANSFER", "DEBIT"]); self.method.currentTextChanged.connect(self.payment_method_changed); self.total_label = QLabel("TOTAL Rp 0"); self.total_label.setObjectName("total"); self.change_label = QLabel("Kembalian: Rp 0")
        for pos, widget in [((0,0),QLabel("Diskon")),((0,1),self.discount),((0,2),QLabel("Metode")),((0,3),self.method),((0,4),QLabel("Bayar")),((0,5),self.paid),((0,6),self.total_label),((1,0),self.change_label)]: pay_l.addWidget(widget,*pos,1,2 if pos==(0,6) else 1)
        checkout = QPushButton("BAYAR & SIMPAN"); checkout.setObjectName("primary"); checkout.clicked.connect(self.checkout); clear = QPushButton("CLEAR"); clear.setObjectName("danger"); clear.clicked.connect(self.clear_cart); pay_l.addWidget(checkout,1,5); pay_l.addWidget(clear,1,7); l.addWidget(pay); return w

    def payment_method_changed(self, method):
        self.paid.setReadOnly(method != "CASH")
        if method != "CASH": self.paid.setValue(float(self.refresh_cart()))
        self.update_change()

    def add_barcode(self):
        code = self.barcode.text().strip()
        if not code: return
        with SessionLocal() as s:
            p = s.query(Product).filter_by(barcode=code, active=True).first()
            if not p: QMessageBox.warning(self, "Produk", "Barcode tidak ditemukan."); return
            q = Decimal(str(self.qty.value())); entry = next((x for x in self.cart if x["product_id"] == p.id), None); current = entry["quantity"] if entry else Decimal("0")
            if current + q > Decimal(str(p.stock)): QMessageBox.warning(self, "Stok", f"Stok {p.name} tidak mencukupi."); return
        if entry: entry["quantity"] += q
        else: self.cart.append({"product_id": p.id, "quantity": q})
        self.barcode.clear(); self.qty.setValue(1); self.refresh_cart(); self.barcode.setFocus()

    def refresh_cart(self):
        self.cart_table.setRowCount(len(self.cart)); subtotal = Decimal("0")
        with SessionLocal() as s:
            for i, item in enumerate(self.cart):
                p = s.get(Product, item["product_id"])
                if not p: continue
                line = Decimal(str(p.selling_price)) * item["quantity"]; subtotal += line
                for c, value in enumerate([p.barcode, p.name, item["quantity"], money(p.selling_price), money(line)]): self.cart_table.setItem(i,c,QTableWidgetItem(str(value)))
        total = max(Decimal("0"), subtotal - Decimal(str(self.discount.value()))); self.total_label.setText(f"TOTAL {money(total)}")
        if self.method.currentText() != "CASH": self.paid.blockSignals(True); self.paid.setValue(float(total)); self.paid.blockSignals(False)
        self.update_change(total); return total

    def update_change(self, total=None):
        if total is None: total = self.refresh_cart() if hasattr(self, "cart_table") else Decimal("0")
        paid = Decimal(str(self.paid.value())); change = max(Decimal("0"), paid-total) if self.method.currentText()=="CASH" else Decimal("0"); self.change_label.setText(f"Kembalian: {money(change)}")

    def clear_cart(self): self.cart.clear(); self.discount.setValue(0); self.paid.setValue(0); self.refresh_cart(); self.barcode.setFocus()

    def checkout(self):
        try:
            if not self.cart: raise ValueError("Keranjang kosong")
            total = self.refresh_cart(); paid = Decimal(str(self.paid.value()))
            if self.method.currentText()=="CASH" and paid < total: raise ValueError("Pembayaran kurang")
            if self.method.currentText()!="CASH": paid=total
            invoice="INV-"+datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            with SessionLocal() as s:
                sale=create_sale(s,self.cart,self.discount.value(),paid,self.method.currentText(),invoice); items=[]
                for item in self.cart:
                    p=s.get(Product,item["product_id"])
                    if p: items.append({"name":p.name,"quantity":item["quantity"],"unit_price":p.selling_price,"line_total":p.selling_price*item["quantity"]})
            printed=print_receipt(self,sale,items)
            message=(f"Transaksi tersimpan dan struk dicetak.\n{sale.invoice_no}\nTotal {money(sale.total)}\nKembalian {money(sale.change)}" if printed else f"Transaksi tersimpan. Struk tidak dicetak.\n{sale.invoice_no}\nTotal {money(sale.total)}")
            QMessageBox.information(self,"Transaksi Berhasil",message); self.clear_cart(); self.refresh_dashboard_data()
        except Exception as exc: QMessageBox.critical(self,"Transaksi gagal",str(exc))

    def refresh_dashboard_data(self): return

    def products(self):
        w=QWidget(); l=QVBoxLayout(w); l.setContentsMargins(18,16,18,18); l.addWidget(self.page_header("Produk","Kelola master barang, harga, kategori, satuan, dan stok awal.")); form_box=QGroupBox("Data Produk"); form=QFormLayout(form_box); self.p_barcode=QLineEdit(); self.p_name=QLineEdit(); self.p_category=QComboBox(); self.p_unit=QComboBox(); self.p_buy=QDoubleSpinBox(); self.p_sell=QDoubleSpinBox(); self.p_stock=QDoubleSpinBox(); self.p_min=QDoubleSpinBox(); self.load_product_options()
        for x in (self.p_buy,self.p_sell): x.setRange(0,999999999)
        for x in (self.p_stock,self.p_min): x.setRange(0,999999999); x.setDecimals(3)
        for a,b in [("Barcode",self.p_barcode),("Nama Produk",self.p_name),("Kategori",self.p_category),("Satuan",self.p_unit),("Harga Beli",self.p_buy),("Harga Jual",self.p_sell),("Stok Awal",self.p_stock),("Stok Minimum",self.p_min)]: form.addRow(a,b)
        l.addWidget(form_box); buttons=QHBoxLayout()
        for text,slot,obj in [("Tambah Produk",self.save_product,"primary"),("Edit Terpilih",self.edit_product,""),("Nonaktifkan",self.deactivate_selected,"danger"),("Form Baru",self.clear_product_form,"")]: b=QPushButton(text); b.setObjectName(obj) if obj else None; b.clicked.connect(slot); buttons.addWidget(b)
        buttons.addStretch(); l.addLayout(buttons); self.product_table=QTableWidget(0,8); self.product_table.setHorizontalHeaderLabels(["ID","Barcode","Nama","Kategori","Satuan","Beli","Jual","Stok"]); self._prepare_table(self.product_table); self.product_table.cellClicked.connect(self.select_product); l.addWidget(self.product_table,1); self.load_products(); return w

    def load_product_options(self):
        with SessionLocal() as s: cats=s.query(Category).filter_by(active=True).order_by(Category.name).all(); units=s.query(Unit).order_by(Unit.name).all()
        self.p_category.clear(); self.p_unit.clear(); self.p_category.addItem("Tanpa Kategori",None); self.p_unit.addItem("Tanpa Satuan",None)
        for x in cats:self.p_category.addItem(x.name,x.id)
        for x in units:self.p_unit.addItem(x.name,x.id)

    def load_products(self):
        with SessionLocal() as s: rows=s.query(Product).order_by(Product.name).all(); cats={x.id:x.name for x in s.query(Category).all()}; units={x.id:x.name for x in s.query(Unit).all()}
        self.product_table.setRowCount(len(rows))
        for i,p in enumerate(rows):
            for c,v in enumerate([p.id,p.barcode,p.name,cats.get(p.category_id,""),units.get(p.unit_id,""),money(p.purchase_price),money(p.selling_price),p.stock]):self.product_table.setItem(i,c,QTableWidgetItem(str(v)))

    def select_product(self,row,_column):
        self.selected_product_id=int(self.product_table.item(row,0).text())
        with SessionLocal() as s:p=s.get(Product,self.selected_product_id)
        if p:
            self.p_barcode.setText(p.barcode); self.p_name.setText(p.name); self.p_buy.setValue(float(p.purchase_price)); self.p_sell.setValue(float(p.selling_price)); self.p_min.setValue(float(p.minimum_stock)); self.p_stock.setValue(float(p.stock)); self.p_category.setCurrentIndex(max(0,self.p_category.findData(p.category_id))); self.p_unit.setCurrentIndex(max(0,self.p_unit.findData(p.unit_id)))

    def save_product(self):
        try:
            with SessionLocal() as s:create_product(s,self.p_barcode.text(),self.p_name.text(),self.p_buy.value(),self.p_sell.value(),self.p_stock.value(),self.p_min.value(),self.p_category.currentData(),self.p_unit.currentData())
            self.load_products(); self.clear_product_form(); QMessageBox.information(self,"Produk","Produk berhasil ditambahkan.")
        except Exception as e: QMessageBox.warning(self,"Produk",str(e))

    def edit_product(self):
        try:
            pid=getattr(self,"selected_product_id",None)
            if not pid: raise ValueError("Pilih produk terlebih dahulu")
            with SessionLocal() as s:update_product(s,pid,barcode=self.p_barcode.text(),name=self.p_name.text(),purchase_price=self.p_buy.value(),selling_price=self.p_sell.value(),minimum_stock=self.p_min.value(),category_id=self.p_category.currentData(),unit_id=self.p_unit.currentData())
            self.load_products(); QMessageBox.information(self,"Produk","Produk diperbarui.")
        except Exception as e: QMessageBox.warning(self,"Produk",str(e))

    def deactivate_selected(self):
        try:
            pid=getattr(self,"selected_product_id",None)
            if not pid: raise ValueError("Pilih produk terlebih dahulu")
            with SessionLocal() as s:deactivate_product(s,pid)
            self.load_products(); self.clear_product_form()
        except Exception as e: QMessageBox.warning(self,"Produk",str(e))

    def clear_product_form(self): self.p_barcode.clear(); self.p_name.clear(); self.p_buy.setValue(0); self.p_sell.setValue(0); self.p_stock.setValue(0); self.p_min.setValue(0); self.p_category.setCurrentIndex(0); self.p_unit.setCurrentIndex(0); self.selected_product_id=None

    def stock_page(self):
        w=QWidget(); l=QVBoxLayout(w); l.setContentsMargins(18,16,18,18); l.addWidget(self.page_header("Stok & Mutasi","Lakukan penyesuaian stok dan pantau status persediaan.")); box=QGroupBox("Mutasi Stok"); f=QHBoxLayout(box); self.stock_product=QComboBox(); self.stock_qty=QDoubleSpinBox(); self.stock_qty.setRange(-999999,999999); self.stock_qty.setDecimals(3); self.stock_ref=QLineEdit(); self.stock_ref.setPlaceholderText("Referensi / nomor opname"); self.load_stock_products(); f.addWidget(self.stock_product,3); f.addWidget(self.stock_qty,1); f.addWidget(self.stock_ref,3); b=QPushButton("Simpan Mutasi"); b.setObjectName("primary"); b.clicked.connect(self.save_stock_adjustment); f.addWidget(b); l.addWidget(box); self.stock_table=QTableWidget(0,5); self.stock_table.setHorizontalHeaderLabels(["Produk","Barcode","Stok","Minimum","Status"]); self._prepare_table(self.stock_table); l.addWidget(self.stock_table,1); self.load_stock_table(); return w

    def load_stock_products(self):
        with SessionLocal() as s: rows=s.query(Product).filter_by(active=True).order_by(Product.name).all()
        self.stock_product.clear()
        for p in rows:self.stock_product.addItem(f"{p.name} | {p.barcode}",p.id)

    def save_stock_adjustment(self):
        try:
            if self.stock_product.currentData() is None:raise ValueError("Belum ada produk aktif")
            if self.stock_qty.value()==0:raise ValueError("Jumlah mutasi tidak boleh 0")
            with SessionLocal() as s:adjust_stock(s,self.stock_product.currentData(),self.stock_qty.value(),"OPNAME",self.stock_ref.text().strip() or None)
            self.stock_qty.setValue(0); self.stock_ref.clear(); self.load_stock_table(); self.load_stock_products(); QMessageBox.information(self,"Stok","Mutasi stok berhasil disimpan.")
        except Exception as e:QMessageBox.warning(self,"Stok",str(e))

    def load_stock_table(self):
        with SessionLocal() as s:rows=stock_summary(s)
        self.stock_table.setRowCount(len(rows))
        for i,x in enumerate(rows):
            for c,v in enumerate([x["name"],x["barcode"],x["stock"],x["minimum_stock"],x["status"]]):self.stock_table.setItem(i,c,QTableWidgetItem(str(v)))

    def purchase_page(self):
        w=QWidget(); l=QVBoxLayout(w); l.setContentsMargins(18,16,18,18); l.addWidget(self.page_header("Pembelian","Catat pembelian supplier dan otomatis tambahkan stok.")); box=QGroupBox("Pembelian Barang"); f=QFormLayout(box); self.buy_product=QComboBox(); self.buy_supplier=QComboBox(); self.buy_qty=QDoubleSpinBox(); self.buy_qty.setRange(0.001,999999); self.buy_qty.setDecimals(3); self.buy_cost=QDoubleSpinBox(); self.buy_cost.setRange(0,999999999); self.buy_invoice=QLineEdit(); self.buy_invoice.setPlaceholderText("Kosongkan untuk nomor otomatis"); self.load_purchase_options()
        for a,b in [("Produk",self.buy_product),("Supplier",self.buy_supplier),("Qty",self.buy_qty),("Harga Beli",self.buy_cost),("No. Invoice",self.buy_invoice)]:f.addRow(a,b)
        l.addWidget(box); b=QPushButton("Simpan Pembelian & Tambah Stok"); b.setObjectName("primary"); b.clicked.connect(self.save_purchase); l.addWidget(b); info=QLabel("Catatan: versi saat ini mencatat satu produk per transaksi pembelian. Multi-item akan menjadi tahap pengembangan berikutnya."); info.setObjectName("pageSubtitle"); l.addWidget(info); l.addStretch(); return w

    def load_purchase_options(self):
        with SessionLocal() as s:products=s.query(Product).filter_by(active=True).order_by(Product.name).all(); suppliers=s.query(Supplier).order_by(Supplier.name).all()
        self.buy_product.clear(); self.buy_supplier.clear()
        for p in products:self.buy_product.addItem(f"{p.name} | {p.barcode}",p.id)
        self.buy_supplier.addItem("Tanpa Supplier",None)
        for sup in suppliers:self.buy_supplier.addItem(sup.name,sup.id)

    def save_purchase(self):
        try:
            if self.buy_product.currentData() is None:raise ValueError("Belum ada produk aktif")
            inv=self.buy_invoice.text().strip() or "PB-"+datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            with SessionLocal() as s:create_purchase(s,[{"product_id":self.buy_product.currentData(),"quantity":self.buy_qty.value(),"unit_cost":self.buy_cost.value()}],self.buy_supplier.currentData(),inv)
            QMessageBox.information(self,"Pembelian",f"Pembelian {inv} tersimpan dan stok bertambah."); self.buy_invoice.clear(); self.buy_qty.setValue(1); self.load_stock_table(); self.load_stock_products(); self.load_products()
        except Exception as e:QMessageBox.warning(self,"Pembelian",str(e))

    def cash_page(self):
        w=QWidget(); l=QVBoxLayout(w); l.setContentsMargins(18,16,18,18); l.addWidget(self.page_header("Kas","Kelola kas masuk dan kas keluar di luar transaksi penjualan.")); box=QGroupBox("Input Kas"); f=QHBoxLayout(box); self.cash_type=QComboBox(); self.cash_type.addItems(["IN","OUT"]); self.cash_amount=QDoubleSpinBox(); self.cash_amount.setRange(0,999999999); self.cash_note=QLineEdit(); self.cash_note.setPlaceholderText("Keterangan"); f.addWidget(QLabel("Jenis"));f.addWidget(self.cash_type);f.addWidget(QLabel("Jumlah"));f.addWidget(self.cash_amount);f.addWidget(self.cash_note,2);b=QPushButton("Simpan Kas");b.setObjectName("primary");b.clicked.connect(self.save_cash);f.addWidget(b);l.addWidget(box);self.cash_label=QLabel();self.cash_label.setObjectName("cardValue");l.addWidget(self.cash_label);l.addStretch();self.refresh_cash();return w

    def save_cash(self):
        try:
            with SessionLocal() as s:record_cash_movement(s,self.cash_type.currentText(),self.cash_amount.value(),note=self.cash_note.text())
            self.cash_amount.setValue(0);self.cash_note.clear();self.refresh_cash();QMessageBox.information(self,"Kas","Mutasi kas tersimpan.")
        except Exception as e:QMessageBox.warning(self,"Kas",str(e))

    def refresh_cash(self):
        with SessionLocal() as s:x=cash_summary(s)
        self.cash_label.setText(f"Kas Masuk {money(x['cash_in'])}   ·   Kas Keluar {money(x['cash_out'])}   ·   Saldo {money(x['balance'])}")

    def report_page(self):
        w=QWidget();l=QVBoxLayout(w);l.setContentsMargins(18,16,18,18);l.addWidget(self.page_header("Laporan","Ringkasan penjualan, kas, stok, dan transaksi terakhir."));bar=QHBoxLayout();refresh=QPushButton("Refresh");refresh.clicked.connect(self.refresh_report);bar.addWidget(refresh);reprint=QPushButton("Cetak Ulang Transaksi Terpilih");reprint.clicked.connect(self.reprint_selected);bar.addWidget(reprint);bar.addStretch();l.addLayout(bar);self.report_text=QTextEdit();self.report_text.setReadOnly(True);l.addWidget(self.report_text,1);self.report_table=QTableWidget(0,5);self.report_table.setHorizontalHeaderLabels(["ID","Invoice","Tanggal","Metode","Total"]);self._prepare_table(self.report_table);l.addWidget(self.report_table,2);self.refresh_report();return w

    def refresh_report(self):
        with SessionLocal() as s:sales=sales_summary(s);cash=cash_summary(s);stock=stock_summary(s);rows=recent_sales(s,100)
        low=sum(1 for x in stock if x["status"]!="AMAN");self.report_text.setHtml(f"<h2>Ringkasan WPOS PRO</h2><p><b>Transaksi:</b> {sales['transactions']} &nbsp;&nbsp; <b>Omzet:</b> {money(sales['omzet'])}</p><p><b>Kas masuk:</b> {money(cash['cash_in'])} &nbsp;&nbsp; <b>Kas keluar:</b> {money(cash['cash_out'])} &nbsp;&nbsp; <b>Saldo:</b> {money(cash['balance'])}</p><p><b>Produk stok perlu perhatian:</b> {low}</p>");self.report_table.setRowCount(len(rows))
        for i,sale in enumerate(rows):
            for c,v in enumerate([sale.id,sale.invoice_no,sale.created_at.strftime("%d/%m/%Y %H:%M:%S"),sale.payment_method,money(sale.total)]):self.report_table.setItem(i,c,QTableWidgetItem(str(v)))

    def reprint_selected(self):
        row=self.report_table.currentRow()
        if row<0:QMessageBox.warning(self,"Cetak Ulang","Pilih transaksi terlebih dahulu.");return
        sale_id=int(self.report_table.item(row,0).text())
        try:
            with SessionLocal() as s:
                sale=s.get(Sale,sale_id)
                if not sale:raise ValueError("Transaksi tidak ditemukan")
                items=[]
                for item in sale.items:
                    p=s.get(Product,item.product_id)
                    if p:items.append({"name":p.name,"quantity":item.quantity,"unit_price":item.unit_price,"line_total":item.line_total})
            if print_receipt(self,sale,items):QMessageBox.information(self,"Cetak Ulang","Struk berhasil dikirim ke printer.")
        except Exception as e:QMessageBox.warning(self,"Cetak Ulang",str(e))

    def settings_page(self):
        w=QWidget();l=QVBoxLayout(w);l.setContentsMargins(18,16,18,18);l.addWidget(self.page_header("Pengaturan Toko","Informasi toko yang digunakan pada struk."));box=QGroupBox("Identitas Toko");form=QFormLayout(box);self.settings_fields={};defaults=get_settings(self._session())
        for key,label in [("store_name","Nama Toko"),("store_address","Alamat"),("store_phone","Telepon"),("receipt_footer","Footer Struk")]:field=QLineEdit(defaults.get(key,""));self.settings_fields[key]=field;form.addRow(label,field)
        l.addWidget(box);save=QPushButton("Simpan Pengaturan");save.setObjectName("primary");save.clicked.connect(self.save_store_settings);l.addWidget(save);l.addStretch();return w

    def _session(self): return _SessionContext(SessionLocal())

    def save_store_settings(self):
        try:
            with SessionLocal() as s:save_settings(s,{key:field.text() for key,field in self.settings_fields.items()})
            QMessageBox.information(self,"Pengaturan","Pengaturan toko berhasil disimpan.")
        except Exception as e:QMessageBox.warning(self,"Pengaturan",str(e))

    def printer_page(self):
        w=QWidget();l=QVBoxLayout(w);l.setContentsMargins(18,16,18,18);l.addWidget(self.page_header("Printer","Printer thermal WPOS PRO · standar 58mm."));box=QGroupBox("Printer Struk · 58mm");f=QFormLayout(box);self.printer_combo=QComboBox();self.printer_combo.addItem("Printer default / pilih saat cetak","")
        for name in available_printers():self.printer_combo.addItem(name,name)
        settings=get_settings(self._session());current=settings.get("printer_name","");idx=self.printer_combo.findData(current)
        if idx>=0:self.printer_combo.setCurrentIndex(idx)
        f.addRow("Printer",self.printer_combo);paper=QLabel("58mm (tetap)");paper.setObjectName("pageSubtitle");f.addRow("Kertas",paper);l.addWidget(box)
        row=QHBoxLayout();save=QPushButton("Simpan Printer");save.setObjectName("primary");save.clicked.connect(self.save_printer_settings);test=QPushButton("Tes Cetak 58mm");test.clicked.connect(lambda:test_print(self,self.printer_combo.currentData() or "","58mm"));row.addWidget(save);row.addWidget(test);row.addStretch();l.addLayout(row);l.addStretch();return w

    def save_printer_settings(self):
        try:
            with SessionLocal() as s:save_settings(s,{"printer_name":self.printer_combo.currentData() or "","receipt_paper":"58mm"})
            QMessageBox.information(self,"Printer","Printer disimpan. Standar kertas WPOS PRO: 58mm.")
        except Exception as e:QMessageBox.warning(self,"Printer",str(e))

    def backup_page(self):
        w=QWidget();l=QVBoxLayout(w);l.setContentsMargins(18,16,18,18);l.addWidget(self.page_header("Backup / Restore","Amankan database lokal sebelum melakukan perubahan besar."));box=QGroupBox("Database");f=QVBoxLayout(box);backup=QPushButton("BUAT BACKUP SEKARANG");backup.setObjectName("primary");backup.clicked.connect(self.do_backup);restore=QPushButton("RESTORE DARI FILE");restore.clicked.connect(self.do_restore);note=QLabel("Backup disimpan di folder data aplikasi. Restore akan mengganti database aktif dan aplikasi harus dijalankan ulang.");note.setWordWrap(True);f.addWidget(backup);f.addWidget(restore);f.addWidget(note);l.addWidget(box);l.addStretch();return w

    def do_backup(self):
        try:path=backup_database();QMessageBox.information(self,"Backup",f"Backup berhasil dibuat:\n{path}")
        except Exception as e:QMessageBox.warning(self,"Backup",str(e))

    def do_restore(self):
        path,_=QFileDialog.getOpenFileName(self,"Pilih Backup","","Database (*.db)")
        if not path:return
        if QMessageBox.question(self,"Konfirmasi Restore","Restore akan mengganti database aktif. Lanjutkan?")!=QMessageBox.Yes:return
        try:engine.dispose();restore_database(path);QMessageBox.information(self,"Restore Berhasil","Database berhasil dipulihkan. Tutup dan jalankan kembali WPOS PRO.")
        except Exception as e:QMessageBox.critical(self,"Restore",str(e))

    def on_tab_changed(self,index):
        title=self.tabs.tabText(index)
        if title=="Produk" and hasattr(self,"product_table"):self.load_product_options();self.load_products()
        elif title=="Stok & Mutasi" and hasattr(self,"stock_table"):self.load_stock_products();self.load_stock_table()
        elif title=="Pembelian":self.load_purchase_options()
        elif title=="Kas":self.refresh_cash()
        elif title=="Laporan":self.refresh_report()


class _SessionContext:
    def __init__(self,session):self.session=session
    def __enter__(self):return self.session
    def __exit__(self,exc_type,exc,tb):self.session.close()
