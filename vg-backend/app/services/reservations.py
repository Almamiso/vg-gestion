from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.db.models.stock import Stock
from app.db.models.reservations import Reservation
from app.db.models.orders import OrderItem


def get_product_onhand(db: Session, location_id: int, produit_id: int) -> float:
    row = db.execute(
        select(Stock.quantite)
        .where(Stock.location_id == location_id, Stock.type_item == "produit", Stock.item_id == produit_id)
    ).scalar_one_or_none()
    return float(row or 0)


def get_reserved_total(db: Session, location_id: int, produit_id: int) -> float:
    total = db.execute(
        select(func.coalesce(func.sum(Reservation.qty), 0.0)).where(
            Reservation.location_id == location_id, Reservation.produit_id == produit_id
        )
    ).scalar_one()
    return float(total or 0)


def get_stock_securite(db: Session, location_id: int, produit_id: int) -> float:
    val = db.execute(
        select(Stock.stock_securite).where(
            Stock.location_id == location_id, Stock.type_item == "produit", Stock.item_id == produit_id
        )
    ).scalar_one_or_none()
    return float(val or 0)


def compute_available(db: Session, location_id: int, produit_id: int) -> float:
    onhand = get_product_onhand(db, location_id, produit_id)
    reserved = get_reserved_total(db, location_id, produit_id)
    stock_securite = get_stock_securite(db, location_id, produit_id)
    return max(0.0, onhand - reserved - stock_securite)


def reserve_order_item(db: Session, order_id: int, location_id: int, item: OrderItem) -> float:
    needed = float(item.qty_ordered) - float(item.qty_reserved)
    if needed <= 0:
        return 0.0
    available = compute_available(db, location_id, item.produit_id)
    to_reserve = min(needed, available)
    if to_reserve <= 0:
        return 0.0
    res = Reservation(order_id=order_id, produit_id=item.produit_id, location_id=location_id, qty=to_reserve)
    item.qty_reserved = float(item.qty_reserved) + to_reserve
    db.add(res)
    db.flush()
    return to_reserve