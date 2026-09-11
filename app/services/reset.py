from sqlalchemy import delete, update

from ..models import (
    CashMovement,
    Category,
    Customer,
    Product,
    Purchase,
    PurchaseItem,
    Sale,
    SaleItem,
    StockMovement,
    Supplier,
    Unit,
)


def _delete_transaction_data(session):
    """Delete transaction/audit rows in FK-safe order."""
    counts = {}
    for model in (SaleItem, Sale, PurchaseItem, Purchase, StockMovement, CashMovement):
        result = session.execute(delete(model))
        counts[model.__tablename__] = result.rowcount or 0
    return counts


def reset_transactions_and_stock(session):
    """Reset sales, purchases, cash and stock movements while keeping master data."""
    counts = _delete_transaction_data(session)
    result = session.execute(update(Product).values(stock=0))
    counts["products_stock_reset"] = result.rowcount or 0
    session.commit()
    return counts


def reset_all_business_data(session):
    """Reset all business data while preserving users and store settings."""
    counts = _delete_transaction_data(session)
    for model in (Product, Customer, Supplier, Category, Unit):
        result = session.execute(delete(model))
        counts[model.__tablename__] = result.rowcount or 0
    session.commit()
    return counts
