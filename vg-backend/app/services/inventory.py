from __future__ import annotations
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.db.models.stock import Stock
from app.db.models.inventory_moves import InventoryMovement
from app.schemas.inventory import InventoryMovementCreate
from app.utils.locking import redis_lock


def apply_movement(db: Session, payload: InventoryMovementCreate) -> dict:
    lock_key = f"lock:stock:{payload.type_item}:{payload.item_id}:{payload.location_id}"
    with redis_lock(lock_key, ttl_seconds=15) as acquired:
        if not acquired:
            raise HTTPException(status_code=409, detail="Stock is locked, retry")
        sign = 1 if payload.direction == '+' else -1
        qty_delta = sign * payload.qty
        existing = db.execute(
            select(Stock).where(
                Stock.location_id == payload.location_id,
                Stock.type_item == payload.type_item,
                Stock.item_id == payload.item_id,
            )
        ).scalar_one_or_none()

        if existing is None:
            if payload.direction == '-':
                raise HTTPException(status_code=400, detail="Cannot decrement non-existing stock")
            existing = Stock(
                location_id=payload.location_id,
                type_item=payload.type_item,
                item_id=payload.item_id,
                quantite=0,
            )
            db.add(existing)
            db.flush()

        new_qty = float(existing.quantite) + qty_delta
        if new_qty < 0:
            raise HTTPException(status_code=400, detail="Insufficient stock")

        existing.quantite = new_qty

        move = InventoryMovement(
            location_id=payload.location_id,
            type_item=payload.type_item,
            item_id=payload.item_id,
            qty=payload.qty,
            direction=payload.direction,
            motif=payload.motif,
            ref_type=payload.ref_type,
            ref_id=payload.ref_id,
        )
        db.add(move)
        db.flush()
        return {"move_id": move.move_id, "new_qty": float(existing.quantite)}


def apply_transfer(db: Session, from_location_id: int, to_location_id: int, type_item: str, item_id: int, qty: float) -> dict:
    if from_location_id == to_location_id:
        raise HTTPException(status_code=400, detail="from and to locations must differ")
    loc_a, loc_b = sorted([from_location_id, to_location_id])
    key_a = f"lock:stock:{type_item}:{item_id}:{loc_a}"
    key_b = f"lock:stock:{type_item}:{item_id}:{loc_b}"
    with redis_lock(key_a) as a:
        if not a:
            raise HTTPException(status_code=409, detail="Source or target stock locked")
        with redis_lock(key_b) as b:
            if not b:
                raise HTTPException(status_code=409, detail="Source or target stock locked")
            apply_movement(db, InventoryMovementCreate(location_id=from_location_id, type_item=type_item, item_id=item_id, qty=qty, direction='-', motif='transfer', ref_type='transfer'))
            apply_movement(db, InventoryMovementCreate(location_id=to_location_id, type_item=type_item, item_id=item_id, qty=qty, direction='+', motif='transfer', ref_type='transfer'))
            return {"status": "ok"}