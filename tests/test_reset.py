from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import (
    CashMovement,
    Category,
    Customer,
    Product,
    Purchase,
    PurchaseItem,
    Sale,
    SaleItem,
    Setting,
    StockMovement,
    Supplier,
    Unit,
    User,
)
from app.services.reset import reset_all_business_data, reset_transactions_and_stock


def make_session():
    db = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(db)
    return sessionmaker(bind=db, autoflush=False, expire_on_commit=False)()


def seed(session):
    user = User(username="admin", password_hash="hash", role="ADMIN", active=True)
    setting = Setting(key="store_name", value="Toko Test")
    category = Category(name="Sembako", active=True)
    unit = Unit(name="PCS")
    supplier = Supplier(name="Supplier Test")
    customer = Customer(name="Customer Test")
    product = Product(barcode="RST-1", name="Produk Test", category_id=None, unit_id=None, stock=12, minimum_stock=2)
    session.add_all([user, setting, category, unit, supplier, customer, product])
    session.flush()
    product.category_id = category.id
    product.unit_id = unit.id
    sale = Sale(invoice_no="INV-RST-1", subtotal=10000, total=10000, paid=10000, change=0, payment_method="CASH")
    session.add(sale)
    session.flush()
    session.add(SaleItem(sale_id=sale.id, product_id=product.id, quantity=1, unit_price=10000, line_total=10000))
    purchase = Purchase(invoice_no="PB-RST-1", supplier_id=supplier.id, total=5000)
    session.add(purchase)
    session.flush()
    session.add(PurchaseItem(purchase_id=purchase.id, product_id=product.id, quantity=2, unit_cost=2500, line_total=5000))
    session.add(StockMovement(product_id=product.id, movement_type="OPNAME", quantity=2, reference="RST"))
    session.add(CashMovement(movement_type="IN", amount=10000, reference="RST"))
    session.commit()


def test_reset_transactions_and_stock_keeps_master_data():
    session = make_session()
    seed(session)
    reset_transactions_and_stock(session)
    assert session.query(Sale).count() == 0
    assert session.query(SaleItem).count() == 0
    assert session.query(Purchase).count() == 0
    assert session.query(PurchaseItem).count() == 0
    assert session.query(StockMovement).count() == 0
    assert session.query(CashMovement).count() == 0
    assert session.query(Product).one().stock == Decimal("0.000")
    assert session.query(Category).count() == 1
    assert session.query(Unit).count() == 1
    assert session.query(User).count() == 1
    assert session.query(Setting).count() == 1


def test_reset_all_business_data_keeps_admin_and_settings():
    session = make_session()
    seed(session)
    reset_all_business_data(session)
    assert session.query(Sale).count() == 0
    assert session.query(Purchase).count() == 0
    assert session.query(StockMovement).count() == 0
    assert session.query(CashMovement).count() == 0
    assert session.query(Product).count() == 0
    assert session.query(Category).count() == 0
    assert session.query(Unit).count() == 0
    assert session.query(Supplier).count() == 0
    assert session.query(Customer).count() == 0
    assert session.query(User).count() == 1
    assert session.query(Setting).count() == 1
