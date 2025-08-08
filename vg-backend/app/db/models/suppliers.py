from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Supplier(Base):
    __tablename__ = "fournisseurs"

    fournisseur_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String, nullable=False)
    contact: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    tel: Mapped[str | None] = mapped_column(String, nullable=True)
    delai_livraison_jours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    conditions_paiement: Mapped[str | None] = mapped_column(String, nullable=True)
    devise: Mapped[str | None] = mapped_column(String, nullable=True)