from pydantic import BaseModel, Field
from typing import List, Optional

class OrderItemCreate(BaseModel):
    produit_id: int
    qty: float = Field(gt=0)

class OrderImport(BaseModel):
    source: str
    type: str
    location_id: int
    items: List[OrderItemCreate]

class OrderCreated(BaseModel):
    order_id: int

class ReserveResponse(BaseModel):
    reserved_total: float

class PickLine(BaseModel):
    order_item_id: int
    qty: float = Field(gt=0)

class PackLine(BaseModel):
    order_item_id: int
    qty: float = Field(gt=0)

class PickRequest(BaseModel):
    items: List[PickLine]

class PackRequest(BaseModel):
    box_label: Optional[str] = None
    items: List[PackLine]

class ShipRequest(BaseModel):
    tracking: Optional[str] = None