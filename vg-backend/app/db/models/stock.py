from sqlalchemy import Integer, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Stock(Base):
    __tablename__ = "stock"

    stock_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.location_id", ondelete="CASCADE"))
    type_item: Mapped[str] = mapped_column(String)
    item_id: Mapped[int] = mapped_column(Integer)
    quantite: Mapped[float] = mapped_column(Numeric(12,4), default=0)
    stock_securite: Mapped[float] = mapped_column(Numeric(12,4), default=0)
    stock_cible: Mapped[float] = mapped_column(Numeric(12,4), default=0)

    __table_args__ = (
        UniqueConstraint("location_id", "type_item", "item_id", name="uq_stock_loc_type_item"),
    )