from sqlalchemy import Integer, String, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Piece(Base):
    __tablename__ = "pieces"

    piece_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    type: Mapped[str | None] = mapped_column(String, nullable=True)
    fournisseur_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("fournisseurs.fournisseur_id"))
    prix_achat: Mapped[float | None] = mapped_column(Numeric(12,4))
    frais_import: Mapped[float | None] = mapped_column(Numeric(12,4))
    prix_landing: Mapped[float | None] = mapped_column(Numeric(12,4))
    actif: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)