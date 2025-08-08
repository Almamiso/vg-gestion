from sqlalchemy import Integer, ForeignKey, BigInteger, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("orders.order_id", ondelete="CASCADE"))
    produit_id: Mapped[int] = mapped_column(Integer, ForeignKey("produits.produit_id"))
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.location_id"))
    qty: Mapped[float] = mapped_column(Numeric(12,4))