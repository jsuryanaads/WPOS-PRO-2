from decimal import Decimal
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Product, Sale, StockMovement
from app.services.products import create_product
from app.services.sales import create_sale


def make_session():
    db = create_engine("sqlite:///:memory:")
    @event.listens_for(db, "connect")
    def enable_fk(dbapi_connection, connection_record):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(db)
    return sessionmaker(bind=db, autoflush=False, expire_on_commit=False)()


def test_non_cash_payment_must_equal_total():
    session = make_session()
    product = Product(barcode="NC-1", name="QRIS Item", selling_price=Decimal("10000"), stock=Decimal("2"))
    session.add(product)
    session.commit()
    with pytest.raises(ValueError, match="non-tunai harus sama"):
        create_sale(session, [{"product_id": product.id, "quantity": 1}], 0, 9000, "QRIS", "INV-NC-1")
    assert session.query(Sale).count() == 0
    assert session.get(Product, product.id).stock == Decimal("2.000")


def test_opening_stock_creates_stock_movement():
    session = make_session()
    product = create_product(session, "OPEN-1", "Produk Awal", 5000, 7000, 12, 2)
    movement = session.query(StockMovement).filter_by(product_id=product.id).one()
    assert movement.movement_type == "OPENING"
    assert movement.quantity == Decimal("12.000")
    assert movement.reference == "STOK-AWAL"
