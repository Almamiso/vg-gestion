from sqlalchemy import BigInteger, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Box(Base):
    __tablename__ = "boxes"

    box_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("orders.order_id", ondelete="CASCADE"))
    label: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str | None] = mapped_column(String, nullable=True)

class BoxItem(Base):
    __tablename__ = "box_items"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    box_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("boxes.box_id", ondelete="CASCADE"))
    produit_id: Mapped[int] = mapped_column(Integer, ForeignKey("produits.produit_id"))
    qty: Mapped[float] = mapped_column(Numeric(12,4))