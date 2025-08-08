from sqlalchemy import Integer, String, ForeignKey, DateTime, func, BigInteger, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    source: Mapped[str | None] = mapped_column(String, nullable=True)
    type: Mapped[str | None] = mapped_column(String, nullable=True)
    location_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("locations.location_id"))
    status: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("orders.order_id", ondelete="CASCADE"))
    produit_id: Mapped[int] = mapped_column(Integer, ForeignKey("produits.produit_id"))
    qty_ordered: Mapped[float] = mapped_column(Numeric(12,4))
    qty_reserved: Mapped[float] = mapped_column(Numeric(12,4), default=0)
    qty_picked: Mapped[float] = mapped_column(Numeric(12,4), default=0)
    qty_packed: Mapped[float] = mapped_column(Numeric(12,4), default=0)
    qty_shipped: Mapped[float] = mapped_column(Numeric(12,4), default=0)

    order: Mapped[Order] = relationship("Order", back_populates="items")