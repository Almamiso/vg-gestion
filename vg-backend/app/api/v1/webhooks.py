from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.shopify import verify_hmac, HEADER_HMAC, HEADER_TOPIC, HEADER_WEBHOOK_ID, HEADER_SHOP_DOMAIN
from app.utils.idempotency import ensure_webhook_event
from app.db.models.orders import Order, OrderItem

router = APIRouter()

@router.post("/webhooks/shopify/orders")
async def shopify_orders(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    sig = request.headers.get(HEADER_HMAC)
    if not verify_hmac(body, sig):
        raise HTTPException(status_code=401, detail="Invalid HMAC")

    event_id = request.headers.get(HEADER_WEBHOOK_ID) or ""
    topic = request.headers.get(HEADER_TOPIC) or "unknown"
    shop = request.headers.get(HEADER_SHOP_DOMAIN) or "unknown"

    payload = await request.json()

    if not event_id:
        # fallback: derive from payload
        event_id = payload.get("id") and str(payload["id"]) or f"{topic}:{shop}:{hash(body)}"

    if not ensure_webhook_event(db, source="shopify", event_id=event_id, payload=payload):
        return {"status": "ok", "duplicate": True}

    # Minimal import: create order and items
    location_id = payload.get("location_id") or None
    order = Order(source=shop, type="B2C", location_id=location_id, status="planned")
    db.add(order)
    db.flush()
    for line in payload.get("line_items", []):
        produit_id = line.get("product_id")
        qty = float(line.get("quantity", 0))
        if not produit_id or qty <= 0:
            continue
        db.add(OrderItem(order_id=order.order_id, produit_id=int(produit_id), qty_ordered=qty))
    db.flush()

    return {"status": "ok", "order_id": order.order_id}