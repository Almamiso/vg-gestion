from pydantic import BaseModel
from typing import Optional, Literal, List

class ProductCreate(BaseModel):
    nom: str
    code: str
    categorie: Optional[str] = None
    prix_vente: Optional[float] = None
    shopify_id_us: Optional[str] = None
    shopify_id_eu: Optional[str] = None
    image_url: Optional[str] = None
    actif: Optional[bool] = True

class BOMItemCreate(BaseModel):
    type_composant: Literal['piece','hardware']
    composant_id: int
    quantite: float
    dechets_pct: float = 0

class ProductOut(BaseModel):
    produit_id: int
    nom: str
    code: str
    categorie: Optional[str]
    prix_vente: Optional[float]
    actif: bool
    bom: List[BOMItemCreate]

    class Config:
        from_attributes = True