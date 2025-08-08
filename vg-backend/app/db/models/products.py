from sqlalchemy import Boolean, Integer, String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Product(Base):
    __tablename__ = "produits"

    produit_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String, nullable=False)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    categorie: Mapped[str | None] = mapped_column(String, nullable=True)
    prix_vente: Mapped[float | None] = mapped_column(Numeric(12,2), nullable=True)
    shopify_id_us: Mapped[str | None] = mapped_column(String, nullable=True)
    shopify_id_eu: Mapped[str | None] = mapped_column(String, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String, nullable=True)
    actif: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)