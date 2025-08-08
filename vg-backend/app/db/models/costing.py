from sqlalchemy import Integer, Numeric, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.db.base import Base

class ProductStandard(Base):
    __tablename__ = "product_standard"

    produit_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    std_time_total_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    std_cost_labor: Mapped[float | None] = mapped_column(Numeric(12,4), nullable=True)
    std_cost_materielles: Mapped[float | None] = mapped_column(Numeric(12,4), nullable=True)
    std_cost_overhead: Mapped[float | None] = mapped_column(Numeric(12,4), nullable=True)
    std_cost_total: Mapped[float | None] = mapped_column(Numeric(12,4), nullable=True)
    mise_a_jour: Mapped[str | None] = mapped_column(DateTime(timezone=True), server_default=func.now())

class CostingEntry(Base):
    __tablename__ = "costing_entries"

    cost_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    mo_id: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("manufacturing_orders.mo_id", ondelete="CASCADE"))
    type: Mapped[str | None] = mapped_column(String, nullable=True)
    montant: Mapped[float | None] = mapped_column(Numeric(12,4), nullable=True)
    devise: Mapped[str | None] = mapped_column(String, nullable=True)
    note: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), server_default=func.now())