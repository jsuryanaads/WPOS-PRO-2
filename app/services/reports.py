from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy import func
from ..models import Sale, SaleItem, Product, StockMovement, CashMovement


def _range(start=None, end=None):
    if start is None:
        start = datetime.min
    if end is None:
        end = datetime.max
    return start, end


def sales_summary(session, start=None, end=None):
    start, end = _range(start, end)
    query = session.query(Sale).filter(Sale.created_at >= start, Sale.created_at <= end)
    sales = query.all()
    omzet = sum((Decimal(str(s.total)) for s in sales), Decimal("0"))
    return {"transactions": len(sales), "omzet": omzet}


def low_stock_count(session):
    return session.query(Product).filter(Product.active == True, Product.stock <= Product.minimum_stock).count()


def cash_summary(session, start=None, end=None):
    start, end = _range(start, end)
    rows = session.query(CashMovement).filter(
        CashMovement.created_at >= start, CashMovement.created_at <= end
    ).all()
    cash_in = sum((Decimal(str(r.amount)) for r in rows if r.movement_type in {"SALE", "IN"}), Decimal("0"))
    cash_out = sum((Decimal(str(r.amount)) for r in rows if r.movement_type in {"OUT", "PURCHASE"}), Decimal("0"))
    return {"cash_in": cash_in, "cash_out": cash_out, "balance": cash_in - cash_out}


def stock_summary(session):
    rows = session.query(Product).filter(Product.active == True).order_by(Product.name).all()
    return [{
        "id": p.id,
        "barcode": p.barcode,
        "name": p.name,
        "stock": Decimal(str(p.stock)),
        "minimum_stock": Decimal(str(p.minimum_stock)),
        "status": "HABIS" if p.stock <= 0 else ("MENIPIS" if p.stock <= p.minimum_stock else "AMAN"),
    } for p in rows]


def recent_sales(session, limit=50):
    limit = max(1, min(int(limit), 500))
    return session.query(Sale).order_by(Sale.created_at.desc()).limit(limit).all()
