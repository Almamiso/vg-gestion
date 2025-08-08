from sqlalchemy import Integer, String, Numeric, ForeignKey, CheckConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    move_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(Integer, ForeignKey("locations.location_id"))
    type_item: Mapped[str] = mapped_column(String)
    item_id: Mapped[int] = mapped_column(Integer)
    qty: Mapped[float] = mapped_column(Numeric(12,4))
    direction: Mapped[str] = mapped_column(String)
    motif: Mapped[str | None] = mapped_column(String, nullable=True)
    ref_type: Mapped[str | None] = mapped_column(String, nullable=True)
    ref_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("direction IN ('+','-')", name="ck_inventory_movements_direction"),
    )