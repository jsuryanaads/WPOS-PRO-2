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
        for r,p in enumerate(rows):
            vals=[p.id,p.barcode,p.name,cats.get(p.category_id,"-"),units.get(p.unit_id,"-"),money(p.purchase_price),money(p.selling_price),str(p.stock)]
            for c,v in enumerate(vals): self.product_table.setItem(r,c,QTableWidgetItem(str(v)))

    def select_product(self,row,_column):
        self.selected_product_id=int(self.product_table.item(row,0).text())
        with SessionLocal() as s:
            p=s.get(Product,self.selected_product_id)
            if not p:return
            self.p_barcode.setText(p.barcode); self.p_name.setText(p.name); self.p_buy.setValue(float(p.purchase_price)); self.p_sell.setValue(float(p.selling_price)); self.p_stock.setValue(float(p.stock)); self.p_min.setValue(float(p.minimum_stock)); self.p_category.setCurrentIndex(max(0,self.p_category.findData(p.category_id))); self.p_unit.setCurrentIndex(max(0,self.p_unit.findData(p.unit_id)))

    def clear_product_form(self):
        self.selected_product_id=None
        self.p_barcode.clear(); self.p_name.clear(); self.p_buy.setValue(0); self.p_sell.setValue(0); self.p_stock.setValue(0); self.p_min.setValue(0)
        if self.p_category.count(): self.p_category.setCurrentIndex(0)
        if self.p_unit.count(): self.p_unit.setCurrentIndex(0)

    def save_product(self):
        try:
            with SessionLocal() as s:
                create_product(s,self.p_barcode.text().strip(),self.p_name.text().strip(),self.p_buy.value(),self.p_sell.value(),self.p_stock.value(),self.p_min.value(),self.p_category.currentData(),self.p_unit.currentData()); self.load_products(); self.clear_product_form(); QMessageBox.information(self,"Produk","Produk berhasil ditambahkan.")
        except Exception as exc: QMessageBox.critical(self,"Produk gagal",str(exc))

    def edit_product(self):
        if not self.selected_product_id:return QMessageBox.information(self,"Produk","Pilih produk terlebih dahulu.")
        try:
            with SessionLocal() as s:
                update_product(s,self.selected_product_id,self.p_barcode.text().strip(),self.p_name.text().strip(),self.p_buy.value(),self.p_sell.value(),self.p_min.value(),self.p_category.currentData(),self.p_unit.currentData()); self.load_products(); self.clear_product_form(); QMessageBox.information(self,"Produk","Produk berhasil diperbarui.")
        except Exception as exc: QMessageBox.critical(self,"Produk gagal",str(exc))

    def deactivate_selected(self):
        if not self.selected_product_id:return QMessageBox.information(self,"Produk","Pilih produk terlebih dahulu.")
        try:
            with SessionLocal() as s: deactivate_product(s,self.selected_product_id); self.load_products(); self.clear_product_form(); QMessageBox.information(self,"Produk","Produk dinonaktifkan.")
        except Exception as exc: QMessageBox.critical(self,"Produk gagal",str(exc))

    def stock_page(self):
        w=QWidget(); l=QVBoxLayout(w); l.addWidget(self.page_header("Stok & Mutasi","Penyesuaian stok dan riwayat pergerakan.")); form=QFormLayout(); self.s_product=QComboBox(); self.s_delta=QDoubleSpinBox(); self.s_delta.setRange(-999999,999999); self.s_delta.setDecimals(3); self.s_ref=QLineEdit(); self.load_stock_products(); form.addRow("Produk",self.s_product); form.addRow("Perubahan Qty",self.s_delta); form.addRow("Referensi",self.s_ref); b=QPushButton("Simpan Mutasi"); b.setObjectName("primary"); b.clicked.connect(self.save_stock); l.addLayout(form); l.addWidget(b); self.stock_table=QTableWidget(0,4); self.stock_table.setHorizontalHeaderLabels(["Produk","Qty","Tipe","Referensi"]); self._prepare_table(self.stock_table); l.addWidget(self.stock_table,1); self.load_stock(); return w

    def load_stock_products(self):
        with SessionLocal() as s: rows=s.query(Product).filter_by(active=True).order_by(Product.name).all()
        self.s_product.clear();
        for p in rows:self.s_product.addItem(p.name,p.id)

    def save_stock(self):
        try:
            with SessionLocal() as s: adjust_stock(s,self.s_product.currentData(),self.s_delta.value(),"ADJUST",self.s_ref.text().strip()); self.load_stock(); self.s_delta.setValue(0); self.s_ref.clear(); QMessageBox.information(self,"Stok","Mutasi tersimpan.")
        except Exception as exc: QMessageBox.critical(self,"Stok gagal",str(exc))

    def load_stock(self):
        with SessionLocal() as s:
            rows=s.query(Sale).order_by(Sale.created_at.desc()).limit(100).all()
        self.stock_table.setRowCount(0)
        for sale in rows:
            for item in sale.items:
                row=self.stock_table.rowCount(); self.stock_table.insertRow(row); values=[item.product.name if item.product else "-",item.quantity,"SALE",sale.invoice_no]
                for c,v in enumerate(values): self.stock_table.setItem(row,c,QTableWidgetItem(str(v)))

    def purchase_page(self):
        w=QWidget(); l=QVBoxLayout(w); l.addWidget(self.page_header("Pembelian","Restock barang dan pemasok.")); form=QFormLayout(); self.pb_supplier=QComboBox(); self.pb_product=QComboBox(); self.pb_qty=QDoubleSpinBox(); self.pb_qty.setRange(0.001,999999); self.pb_qty.setDecimals(3); self.pb_cost=QDoubleSpinBox(); self.pb_cost.setRange(0,999999999); self.pb_ref=QLineEdit(); self.load_purchase_options();
        for a,b in [("Supplier",self.pb_supplier),("Produk",self.pb_product),("Qty",self.pb_qty),("Harga Beli",self.pb_cost),("Referensi",self.pb_ref)]: form.addRow(a,b)
        l.addLayout(form); b=QPushButton("Simpan Pembelian"); b.setObjectName("primary"); b.clicked.connect(self.save_purchase); l.addWidget(b); return w

    def load_purchase_options(self):
        with SessionLocal() as s: sups=s.query(Supplier).filter_by(active=True).order_by(Supplier.name).all(); prods=s.query(Product).filter_by(active=True).order_by(Product.name).all()
        self.pb_supplier.clear(); self.pb_product.clear();
        for x in sups:self.pb_supplier.addItem(x.name,x.id)
        for x in prods:self.pb_product.addItem(x.name,x.id)

    def save_purchase(self):
        try:
            with SessionLocal() as s: create_purchase(s,[{"product_id":self.pb_product.currentData(),"quantity":self.pb_qty.value(),"unit_cost":self.pb_cost.value()}],self.pb_supplier.currentData(),self.pb_ref.text().strip()); self.load_stock(); QMessageBox.information(self,"Pembelian","Pembelian tersimpan.")
        except Exception as exc: QMessageBox.critical(self,"Pembelian gagal",str(exc))

    def cash_page(self):
        w=QWidget(); l=QVBoxLayout(w); l.addWidget(self.page_header("Kas","Arus kas masuk dan keluar.")); form=QFormLayout(); self.cash_type=QComboBox(); self.cash_type.addItems(["IN","OUT"]); self.cash_amount=QDoubleSpinBox(); self.cash_amount.setRange(0.01,999999999); self.cash_ref=QLineEdit(); self.cash_note=QLineEdit();
        for a,b in [("Tipe",self.cash_type),("Jumlah",self.cash_amount),("Referensi",self.cash_ref),("Keterangan",self.cash_note)]: form.addRow(a,b)
        l.addLayout(form); b=QPushButton("Simpan Kas"); b.setObjectName("primary"); b.clicked.connect(self.save_cash); l.addWidget(b); self.cash_summary_label=QLabel(); l.addWidget(self.cash_summary_label); self.refresh_cash(); return w

    def save_cash(self):
        try:
            with SessionLocal() as s: record_cash_movement(s,self.cash_type.currentText(),self.cash_amount.value(),self.cash_ref.text().strip(),self.cash_note.text().strip()); self.refresh_cash(); self.cash_amount.setValue(0); self.cash_ref.clear(); self.cash_note.clear(); QMessageBox.information(self,"Kas","Mutasi kas tersimpan.")
        except Exception as exc: QMessageBox.critical(self,"Kas gagal",str(exc))

    def refresh_cash(self):
        with SessionLocal() as s: x=cash_summary(s); self.cash_summary_label.setText(f"Masuk {money(x['cash_in'])} · Keluar {money(x['cash_out'])} · Saldo {money(x['balance'])}")

    def report_page(self):
        w=QWidget(); l=QVBoxLayout(w); l.addWidget(self.page_header("Laporan","Ringkasan penjualan, stok, dan kas.")); self.report_label=QLabel(); l.addWidget(self.report_label); b=QPushButton("Refresh Laporan"); b.clicked.connect(self.refresh_report); l.addWidget(b); self.refresh_report(); return w

    def refresh_report(self):
        with SessionLocal() as s: a=sales_summary(s); c=cash_summary(s); l=low_stock_count(s); self.report_label.setText(f"Transaksi {a['transactions']} · Omzet {money(a['omzet'])} · Stok menipis/habis {l} · Saldo kas {money(c['balance'])}")

    def settings_page(self):
        w=QWidget(); l=QVBoxLayout(w); l.addWidget(self.page_header("Pengaturan Toko","Identitas toko dan preferensi aplikasi.")); form=QFormLayout(); self.store_name=QLineEdit(); self.address=QTextEdit(); self.phone=QLineEdit(); self.load_settings_form(); form.addRow("Nama Toko",self.store_name); form.addRow("Alamat",self.address); form.addRow("Telepon",self.phone); l.addLayout(form); b=QPushButton("Simpan Pengaturan"); b.setObjectName("primary"); b.clicked.connect(self.save_settings_form); l.addWidget(b); return w

    def load_settings_form(self):
        with SessionLocal() as s: x=get_settings(s)
        self.store_name.setText(str(x.get("store_name", "TOKO SEMBAKO"))); self.address.setPlainText(str(x.get("address", ""))); self.phone.setText(str(x.get("phone", "")))

    def save_settings_form(self):
        try:
            with SessionLocal() as s: save_settings(s,{"store_name":self.store_name.text().strip(),"address":self.address.toPlainText().strip(),"phone":self.phone.text().strip()}); QMessageBox.information(self,"Pengaturan","Pengaturan tersimpan.")
        except Exception as exc: QMessageBox.critical(self,"Pengaturan gagal",str(exc))

    def printer_page(self):
        w=QWidget(); l=QVBoxLayout(w); l.addWidget(self.page_header("Printer","Pilih printer thermal untuk struk.")); self.printer=QComboBox(); self.printer.addItems(available_printers()); l.addWidget(self.printer); b=QPushButton("Test Print"); b.clicked.connect(lambda:test_print(self.printer.currentText())); l.addWidget(b); return w

    def backup_page(self):
        w=QWidget(); l=QVBoxLayout(w); l.addWidget(self.page_header("Backup / Restore","Cadangkan dan pulihkan database lokal.")); backup=QPushButton("Backup Database"); backup.setObjectName("primary"); backup.clicked.connect(self.do_backup); restore=QPushButton("Restore Database"); restore.setObjectName("danger"); restore.clicked.connect(self.do_restore); l.addWidget(backup); l.addWidget(restore); return w

    def do_backup(self):
        try:
            path=QFileDialog.getSaveFileName(self,"Backup Database","wpos-backup.db","SQLite (*.db)")[0]
            if not path:return
            with SessionLocal() as s: backup_database(s,path)
            QMessageBox.information(self,"Backup","Backup berhasil disimpan.")
        except Exception as exc: QMessageBox.critical(self,"Backup gagal",str(exc))

    def do_restore(self):
        try:
            path=QFileDialog.getOpenFileName(self,"Restore Database","","SQLite (*.db)")[0]
            if not path:return
            if QMessageBox.question(self,"Restore","Restore akan mengganti database aktif. Lanjutkan?",QMessageBox.Yes|QMessageBox.No,QMessageBox.No)!=QMessageBox.Yes:return
            restore_database(path)
            QMessageBox.information(self,"Restore","Restore selesai. Aplikasi akan ditutup untuk menerapkan database."); self.close()
        except Exception as exc: QMessageBox.critical(self,"Restore gagal",str(exc)

    def on_tab_changed(self,index):
        if index==2:self.load_products()
        elif index==3:self.load_stock()
        elif index==4:self.load_purchase_options()
        elif index==5:self.refresh_cash()
        elif index==6:self.refresh_report()
        elif index==7:self.load_settings_form()
