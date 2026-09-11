from decimal import Decimal
import pytest
from sqlalchemy import create_engine, inspect, event
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Product, Sale, SaleItem, StockMovement, Supplier, User
from app.services.auth import hash_password, verify_password
from app.services.sales import create_sale
from app.services.stock import adjust_stock
from app.services.purchases import create_purchase
from app.services.reports import cash_summary, stock_summary
from app.services.users import ROLES, create_user, set_user_active
from app.ui.modern_main_window import ModernMainWindow


def make_session():
    engine = create_engine("sqlite:///:memory:")
    @event.listens_for(engine, "connect")
    def enable_fk(dbapi_connection, connection_record):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)()


def test_password_hashing():
    h = hash_password("secret")
    assert verify_password("secret", h)
    assert not verify_password("wrong", h)


def test_required_tables_and_constraints():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    tables = set(inspect(engine).get_table_names())
    assert {"users", "products", "sales", "sale_items", "purchases", "purchase_items", "stock_movements", "cash_movements", "settings"}.issubset(tables)
    assert any(c.name == "ck_products_stock_nonnegative" for c in Product.__table__.constraints)
    assert any(c.name == "ck_sale_items_quantity_positive" for c in SaleItem.__table__.constraints)


def test_money_math():
    assert Decimal("10.00") * Decimal("2") == Decimal("20.00")


def test_duplicate_cart_rows_cannot_bypass_stock():
    session = make_session()
    product = Product(barcode="8990001", name="Beras", selling_price=Decimal("10000"), stock=Decimal("5"))
    session.add(product)
    session.commit()
    with pytest.raises(ValueError, match="tidak mencukupi"):
        create_sale(session, [
            {"product_id": product.id, "quantity": "3"},
            {"product_id": product.id, "quantity": "3"},
        ], Decimal("0"), Decimal("20000"), "CASH", "INV-001")
    assert session.query(Sale).count() == 0
    assert session.get(Product, product.id).stock == Decimal("5.000")


def test_sale_is_atomic_on_failure():
    session = make_session()
    product = Product(barcode="8990002", name="Gula", selling_price=Decimal("15000"), stock=Decimal("2"))
    session.add(product)
    session.commit()
    with pytest.raises(ValueError, match="Pembayaran kurang"):
        create_sale(session, [{"product_id": product.id, "quantity": "1"}], Decimal("0"), Decimal("1"), "CASH", "INV-002")
    assert session.query(Sale).count() == 0
    assert session.query(StockMovement).count() == 0
    assert session.get(Product, product.id).stock == Decimal("2.000")


def test_stock_adjustment_records_movement():
    session = make_session()
    product = Product(barcode="8990003", name="Minyak", selling_price=Decimal("18000"), stock=Decimal("10"))
    session.add(product)
    session.commit()
    adjust_stock(session, product.id, Decimal("-2"), "OPNAME", "SO-001")
    assert session.get(Product, product.id).stock == Decimal("8.000")
    movement = session.query(StockMovement).one()
    assert movement.quantity == Decimal("-2.000")
    assert movement.reference == "SO-001"


def test_purchase_validates_supplier_and_updates_stock():
    session = make_session()
    supplier = Supplier(name="Supplier A")
    product = Product(barcode="8990004", name="Tepung", selling_price=Decimal("12000"), stock=Decimal("2"))
    session.add_all([supplier, product])
    session.commit()
    purchase = create_purchase(session, [{"product_id": product.id, "quantity": "3", "unit_cost": "7000"}], supplier.id, "PB-001")
    assert purchase.total == Decimal("21000.00")
    assert session.get(Product, product.id).stock == Decimal("5.000")
    assert session.query(StockMovement).one().movement_type == "PURCHASE"
    with pytest.raises(ValueError, match="Supplier tidak ditemukan"):
        create_purchase(session, [{"product_id": product.id, "quantity": "1", "unit_cost": "7000"}], 99999, "PB-002")


def test_non_cash_sale_does_not_increase_cash_balance():
    session = make_session()
    product = Product(barcode="8990005", name="Susu", selling_price=Decimal("10000"), stock=Decimal("3"))
    session.add(product)
    session.commit()
    create_sale(session, [{"product_id": product.id, "quantity": "1"}], Decimal("0"), Decimal("10000"), "QRIS", "INV-003")
    summary = cash_summary(session)
    assert summary["cash_in"] == Decimal("0")
    assert summary["balance"] == Decimal("0")


def test_stock_summary_statuses():
    session = make_session()
    session.add_all([
        Product(barcode="A", name="A", stock=0, minimum_stock=2),
        Product(barcode="B", name="B", stock=1, minimum_stock=2),
        Product(barcode="C", name="C", stock=5, minimum_stock=2),
    ])
    session.commit()
    statuses = {row["name"]: row["status"] for row in stock_summary(session)}
    assert statuses == {"A": "HABIS", "B": "MENIPIS", "C": "AMAN"}


def test_navigation_has_unique_contiguous_page_indexes():
    entries = [entry for _section, items in ModernMainWindow.NAVIGATION for entry in items]
    indexes = [entry[2] for entry in entries]
    assert len(entries) == 14
    assert sorted(indexes) == list(range(14))
    assert len(set(indexes)) == 14
    expected = {
        0: "Dashboard", 1: "Kasir", 2: "Produk", 3: "Stok & Mutasi", 4: "Pembelian",
        5: "Kas", 6: "Laporan", 7: "Pengaturan Toko", 8: "Printer", 9: "Backup / Restore",
        10: "Kategori", 11: "Satuan", 12: "Supplier", 13: "Pelanggan",
    }
    assert {index: ModernMainWindow._title_for(index) for index in range(14)} == expected


def test_supported_roles_are_stable():
    assert ROLES == ("ADMIN", "PENGELOLA", "TEKNISI")


def test_admin_cannot_be_left_without_active_admin():
    session = make_session()
    admin = User(username="admin", password_hash=hash_password("secret"), role="ADMIN", active=True)
    session.add(admin)
    session.commit()
    with pytest.raises(ValueError, match="Minimal satu Administrator aktif"):
        set_user_active(session, admin.id, False, actor_user_id=999)
    assert session.get(User, admin.id).active is True


def test_user_creation_rejects_invalid_role():
    session = make_session()
    with pytest.raises(ValueError, match="Role tidak valid"):
        create_user(session, "badrole", "secret", "INVALID")
