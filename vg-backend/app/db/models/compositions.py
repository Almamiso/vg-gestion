from sqlalchemy import Integer, String, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Composition(Base):
    __tablename__ = "compositions"

    composition_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produit_id: Mapped[int] = mapped_column(Integer, ForeignKey("produits.produit_id", ondelete="CASCADE"))
    type_composant: Mapped[str] = mapped_column(String)
    composant_id: Mapped[int] = mapped_column(Integer)
    quantite: Mapped[float] = mapped_column(Numeric(12,4))
    dechets_pct: Mapped[float] = mapped_column(Numeric(6,4), default=0)

    __table_args__ = (
        CheckConstraint("type_composant IN ('piece','hardware')", name="ck_compositions_type"),
    )