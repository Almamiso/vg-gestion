from sqlalchemy import Integer, String, ForeignKey, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Event(Base):
    __tablename__ = "evenements"

    evenement_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[str | None] = mapped_column(String, nullable=True)
    date_debut: Mapped[str | None] = mapped_column(Date, nullable=True)
    date_fin: Mapped[str | None] = mapped_column(Date, nullable=True)
    location_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("locations.location_id"))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

class EventProduct(Base):
    __tablename__ = "evenement_produits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    evenement_id: Mapped[int] = mapped_column(Integer, ForeignKey("evenements.evenement_id", ondelete="CASCADE"))
    produit_id: Mapped[int] = mapped_column(Integer, ForeignKey("produits.produit_id"))
    quantite_cible: Mapped[int] = mapped_column(Integer)
    priorite: Mapped[str | None] = mapped_column(String, nullable=True)