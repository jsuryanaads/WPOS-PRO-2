from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, DateTime, ForeignKey, Boolean, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=False)
    role: Mapped[str] = mapped_column(String(30), default="ADMIN", nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Unit(Base):
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("purchase_price >= 0", name="ck_products_purchase_price_nonnegative"),
        CheckConstraint("selling_price >= 0", name="ck_products_selling_price_nonnegative"),
        CheckConstraint("stock >= 0", name="ck_products_stock_nonnegative"),
        CheckConstraint("minimum_stock >= 0", name="ck_products_minimum_stock_nonnegative"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    barcode: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id"))
    unit_id: Mapped[int | None] = mapped_column(ForeignKey("units.id"))
    purchase_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    selling_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    stock: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=0, nullable=False)
    minimum_stock: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=0, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(String(300))


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(50))
    address: Mapped[str | None] = mapped_column(String(300))


class Sale(Base):
    __tablename__ = "sales"
    __table_args__ = (
        CheckConstraint("subtotal >= 0", name="ck_sales_subtotal_nonnegative"),
        CheckConstraint("discount >= 0", name="ck_sales_discount_nonnegative"),
        CheckConstraint("total >= 0", name="ck_sales_total_nonnegative"),
        CheckConstraint("paid >= 0", name="ck_sales_paid_nonnegative"),
        CheckConstraint("change >= 0", name="ck_sales_change_nonnegative"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_no: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    discount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    paid: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    change: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(30), default="CASH", nullable=False)
    items: Mapped[list["SaleItem"]] = relationship(back_populates="sale", cascade="all, delete-orphan")


class SaleItem(Base):
    __tablename__ = "sale_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_sale_items_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="ck_sale_items_unit_price_nonnegative"),
        CheckConstraint("discount >= 0", name="ck_sale_items_discount_nonnegative"),
        CheckConstraint("line_total >= 0", name="ck_sale_items_line_total_nonnegative"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    discount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    sale: Mapped["Sale"] = relationship(back_populates="items")


class Purchase(Base):
    __tablename__ = "purchases"
    __table_args__ = (CheckConstraint("total >= 0", name="ck_purchases_total_nonnegative"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    invoice_no: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    supplier_id: Mapped[int | None] = mapped_column(ForeignKey("suppliers.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0, nullable=False)
    items: Mapped[list["PurchaseItem"]] = relationship(back_populates="purchase", cascade="all, delete-orphan")


class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_purchase_items_quantity_positive"),
        CheckConstraint("unit_cost >= 0", name="ck_purchase_items_unit_cost_nonnegative"),
        CheckConstraint("line_total >= 0", name="ck_purchase_items_line_total_nonnegative"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    purchase: Mapped["Purchase"] = relationship(back_populates="items")


class StockMovement(Base):
    __tablename__ = "stock_movements"
    __table_args__ = (CheckConstraint("quantity != 0", name="ck_stock_movements_quantity_nonzero"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    movement_type: Mapped[str] = mapped_column(String(30), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), nullable=False)
    reference: Mapped[str | None] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)


class CashMovement(Base):
    __tablename__ = "cash_movements"
    __table_args__ = (CheckConstraint("amount > 0", name="ck_cash_movements_amount_positive"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    movement_type: Mapped[str] = mapped_column(String(30), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    reference: Mapped[str | None] = mapped_column(String(100))
    note: Mapped[str | None] = mapped_column(String(300))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)


class Setting(Base):
    __tablename__ = "settings"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(Text, default="", nullable=False)
