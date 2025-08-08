from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models.stock import Stock
from app.schemas.inventory import InventoryMovementCreate, StockRecord, TransferCreate
from app.services.inventory import apply_movement, apply_transfer

router = APIRouter()

@router.get("/stock", response_model=list[StockRecord])
def get_stock(location_id: int | None = None, type_item: str | None = None, item_id: int | None = None, db: Session = Depends(get_db)):
    stmt = select(Stock)
    if location_id is not None:
        stmt = stmt.where(Stock.location_id == location_id)
    if type_item is not None:
        stmt = stmt.where(Stock.type_item == type_item)
    if item_id is not None:
        stmt = stmt.where(Stock.item_id == item_id)
    rows = db.execute(stmt).scalars().all()
    return rows

@router.post("/movements")
def create_movement(payload: InventoryMovementCreate, db: Session = Depends(get_db)):
    return apply_movement(db, payload)

@router.post("/transfer")
def transfer_stock(payload: TransferCreate, db: Session = Depends(get_db)):
    return apply_transfer(db, payload.from_location_id, payload.to_location_id, payload.type_item, payload.item_id, payload.qty)