from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.db.models.orders import Order, OrderItem
from app.db.models.boxes import Box, BoxItem
from app.db.models.inventory_moves import InventoryMovement
from app.schemas.orders import OrderImport, OrderCreated, ReserveResponse, PickRequest, PackRequest, ShipRequest
from app.services.reservations import reserve_order_item
from app.utils.locking import redis_lock

router = APIRouter()

@router.post("/orders/import", response_model=OrderCreated)
def import_order(payload: OrderImport, db: Session = Depends(get_db)):
    order = Order(source=payload.source, type=payload.type, location_id=payload.location_id, status="planned")
    db.add(order)
    db.flush()
    for it in payload.items:
        db.add(OrderItem(order_id=order.order_id, produit_id=it.produit_id, qty_ordered=it.qty))
    db.flush()
    return {"order_id": order.order_id}

@router.post("/orders/{order_id}/reserve", response_model=ReserveResponse)
def reserve(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    lock_key = f"lock:order:{order_id}"
    with redis_lock(lock_key, ttl_seconds=15) as acquired:
        if not acquired:
            raise HTTPException(status_code=409, detail="Order is locked, retry")
        reserved_total = 0.0
        items = db.execute(select(OrderItem).where(OrderItem.order_id == order_id)).scalars().all()
        for item in items:
            reserved_total += reserve_order_item(db, order_id, order.location_id or 0, item)
        return {"reserved_total": reserved_total}

@router.post("/orders/{order_id}/pick")
def pick(order_id: int, payload: PickRequest, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    with redis_lock(f"lock:order:{order_id}") as acquired:
        if not acquired:
            raise HTTPException(status_code=409, detail="Order is locked, retry")
        for line in payload.items:
            item = db.get(OrderItem, line.order_item_id)
            if not item or item.order_id != order_id:
                raise HTTPException(status_code=400, detail="Invalid order item")
            remaining = float(item.qty_ordered) - float(item.qty_picked)
            if line.qty > remaining:
                raise HTTPException(status_code=400, detail="Pick qty exceeds remaining")
            # decrement finished goods stock
            move = InventoryMovement(location_id=order.location_id, type_item='produit', item_id=item.produit_id, qty=line.qty, direction='-', motif='pick', ref_type='order', ref_id=order_id)
            db.add(move)
            item.qty_picked = float(item.qty_picked) + line.qty
        order.status = "picking"
        db.flush()
        return {"status": order.status}

@router.post("/orders/{order_id}/pack")
def pack(order_id: int, payload: PackRequest, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    with redis_lock(f"lock:order:{order_id}") as acquired:
        if not acquired:
            raise HTTPException(status_code=409, detail="Order is locked, retry")
        box = Box(order_id=order_id, label=payload.box_label, status="open")
        db.add(box)
        db.flush()
        for line in payload.items:
            item = db.get(OrderItem, line.order_item_id)
            if not item or item.order_id != order_id:
                raise HTTPException(status_code=400, detail="Invalid order item")
            remaining = float(item.qty_picked) - float(item.qty_packed)
            if line.qty > remaining:
                raise HTTPException(status_code=400, detail="Pack qty exceeds picked")
            db.add(BoxItem(box_id=box.box_id, produit_id=item.produit_id, qty=line.qty))
            item.qty_packed = float(item.qty_packed) + line.qty
        order.status = "packing"
        db.flush()
        return {"box_id": box.box_id, "status": order.status}

@router.post("/orders/{order_id}/ship")
def ship(order_id: int, payload: ShipRequest, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    with redis_lock(f"lock:order:{order_id}") as acquired:
        if not acquired:
            raise HTTPException(status_code=409, detail="Order is locked, retry")
        items = db.execute(select(OrderItem).where(OrderItem.order_id == order_id)).scalars().all()
        for item in items:
            remaining = float(item.qty_packed) - float(item.qty_shipped)
            if remaining > 0:
                item.qty_shipped = float(item.qty_shipped) + remaining
        order.status = "shipped"
        db.flush()
        return {"status": order.status}