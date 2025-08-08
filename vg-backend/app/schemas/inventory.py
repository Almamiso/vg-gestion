from pydantic import BaseModel, Field
from typing import Optional, Literal

class InventoryMovementCreate(BaseModel):
    location_id: int
    type_item: Literal['piece','hardware','produit']
    item_id: int
    qty: float = Field(gt=0)
    direction: Literal['+','-']
    motif: Optional[str] = None
    ref_type: Optional[str] = None
    ref_id: Optional[int] = None

class StockFilter(BaseModel):
    location_id: Optional[int] = None
    type_item: Optional[Literal['piece','hardware','produit']] = None
    item_id: Optional[int] = None

class StockRecord(BaseModel):
    location_id: int
    type_item: str
    item_id: int
    quantite: float
    stock_securite: float
    stock_cible: float

    class Config:
        from_attributes = True

class TransferCreate(BaseModel):
    from_location_id: int
    to_location_id: int
    type_item: Literal['piece','hardware','produit']
    item_id: int
    qty: float = Field(gt=0)