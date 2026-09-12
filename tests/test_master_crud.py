import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QMessageBox
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Category, Customer, Product, Purchase, Supplier, Unit
from app.ui.master_data import SimpleMaster
import app.ui.master_data as master_data


def make_session():
    db = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(db)
    return sessionmaker(bind=db, autoflush=False, expire_on_commit=False)()


def test_master_crud_create_edit_delete(monkeypatch):
    session = make_session()
    monkeypatch.setattr(master_data, "SessionLocal", lambda: session)
    app = QApplication.instance() or QApplication([])
    page = SimpleMaster(Category, "Kategori", ["Name"])

    page.inputs[0].setText("Minuman")
    page.save()
    row = page.table.rowCount() - 1
    page.select_row(row)
    assert page.selected_id is not None
    assert page.inputs[0].text() == "Minuman"

    page.inputs[0].setText("Minuman Dingin")
    page.save()
    assert session.query(Category).filter_by(name="Minuman Dingin").count() == 1
    assert session.query(Category).filter_by(name="Minuman").count() == 0

    # Patch the page-level confirmation hook rather than the Qt static method.
    # PySide6's QMessageBox.question can remain modal under offscreen pytest,
    # which makes the test hang even though the delete path itself is correct.
    monkeypatch.setattr(page, "_confirm_delete", lambda _name: True)
    page.delete_selected()
    assert session.query(Category).count() == 0


def test_master_delete_blocks_referenced_records(monkeypatch):
    session = make_session()
    category = Category(name="Sembako")
    unit = Unit(name="PCS")
    supplier = Supplier(name="Supplier A")
    session.add_all([category, unit, supplier])
    session.commit()
    product = Product(barcode="REF-1", name="Beras", category_id=category.id, unit_id=unit.id, selling_price=10000, stock=1)
    session.add(product)
    session.commit()
    purchase = Purchase(invoice_no="PUR-REF-1", supplier_id=supplier.id, total=10000)
    session.add(purchase)
    session.commit()

    monkeypatch.setattr(master_data, "SessionLocal", lambda: session)
    monkeypatch.setattr(QMessageBox, "question", lambda *args, **kwargs: QMessageBox.Yes)
    monkeypatch.setattr(QMessageBox, "warning", lambda *args, **kwargs: None)
    app = QApplication.instance() or QApplication([])

    category_page = SimpleMaster(Category, "Kategori", ["Name"])
    category_page.select_row(0)
    category_page.delete_selected()
    assert session.get(Category, category.id) is not None

    unit_page = SimpleMaster(Unit, "Satuan", ["Name"])
    unit_page.select_row(0)
    unit_page.delete_selected()
    assert session.get(Unit, unit.id) is not None

    supplier_page = SimpleMaster(Supplier, "Supplier", ["Name", "Phone", "Address"])
    supplier_page.select_row(0)
    supplier_page.delete_selected()
    assert session.get(Supplier, supplier.id) is not None


def test_customer_can_be_deleted(monkeypatch):
    session = make_session()
    customer = Customer(name="Pelanggan A", phone="0800", address="Alamat")
    session.add(customer)
    session.commit()
    monkeypatch.setattr(master_data, "SessionLocal", lambda: session)
    monkeypatch.setattr(QMessageBox, "question", lambda *args, **kwargs: QMessageBox.Yes)
    app = QApplication.instance() or QApplication([])

    page = SimpleMaster(Customer, "Pelanggan", ["Name", "Phone", "Address"])
    page.select_row(0)
    page.delete_selected()
    assert session.get(Customer, customer.id) is None
