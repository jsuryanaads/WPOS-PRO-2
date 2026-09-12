from decimal import Decimal
from unittest.mock import patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import Product, Setting, User
from app.services.products import create_product
from app.services.purchases import create_purchase
from app.services.settings import set_setting
from app.services.stock import adjust_stock
from app.services.users import create_user


def make_session():
    db = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(db)
    return sessionmaker(bind=db, autoflush=False, expire_on_commit=False)()


def test_product_rejects_non_finite_decimal_values():
    session = make_session()
    with pytest.raises(ValueError, match="Harga jual tidak valid"):
        create_product(session, "FIN-1", "Produk Finite", selling_price="NaN")
    with pytest.raises(ValueError, match="Stok tidak valid"):
        create_product(session, "FIN-2", "Produk Finite", stock="Infinity")
    assert session.query(Product).count() == 0


def test_purchase_rejects_non_finite_values():
    session = make_session()
    product = Product(barcode="PUR-1", name="Produk Pembelian", selling_price=10000, stock=0)
    session.add(product)
    session.commit()

    with pytest.raises(ValueError, match="Jumlah tidak valid"):
        create_purchase(session, [{"product_id": product.id, "quantity": "NaN", "unit_cost": 5000}], None, "PUR-FIN-1")
    with pytest.raises(ValueError, match="Harga pembelian tidak valid"):
        create_purchase(session, [{"product_id": product.id, "quantity": 1, "unit_cost": "Infinity"}], None, "PUR-FIN-2")
    assert session.get(Product, product.id).stock == Decimal("0.000")


def test_stock_rejects_non_finite_values():
    session = make_session()
    product = Product(barcode="STK-1", name="Produk Stok", selling_price=10000, stock=2)
    session.add(product)
    session.commit()

    with pytest.raises(ValueError, match="Jumlah stok tidak valid"):
        adjust_stock(session, product.id, "NaN")
    with pytest.raises(ValueError, match="Jumlah stok tidak valid"):
        adjust_stock(session, product.id, "-Infinity")
    assert session.get(Product, product.id).stock == Decimal("2.000")


def test_create_user_rolls_back_failed_commit():
    session = make_session()
    with patch.object(session, "commit", side_effect=RuntimeError("forced commit failure")):
        with pytest.raises(RuntimeError, match="forced commit failure"):
            create_user(session, "rollback-user", "secret", "KASIR", name="Rollback User")
    assert session.query(User).filter_by(username="rollback-user").count() == 0
    assert not session.new


def test_set_setting_rolls_back_failed_commit():
    session = make_session()
    with patch.object(session, "commit", side_effect=RuntimeError("forced commit failure")):
        with pytest.raises(RuntimeError, match="forced commit failure"):
            set_setting(session, "store_name", "Rollback Store")
    assert session.query(Setting).filter_by(key="store_name").count() == 0
    assert not session.new
