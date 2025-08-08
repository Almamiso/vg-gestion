from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from app.db.session import get_db
from app.db.models.manufacturing import ManufacturingOrder, MOProduct, MOComponent
from app.db.models.products import Product
from app.db.models.compositions import Composition
from app.db.models.inventory_moves import InventoryMovement

router = APIRouter()

@router.post("/mo")
def create_mo(payload: dict, db: Session = Depends(get_db)):
    location_id = payload.get("location_id")
    produits = payload.get("produits", [])
    due_date = payload.get("due_date")
    mo = ManufacturingOrder(location_id=location_id, status="planned", due_date=due_date)
    db.add(mo)
    db.flush()
    for line in produits:
        mp = MOProduct(mo_id=mo.mo_id, produit_id=line["produit_id"], qty_to_build=line["qty_to_build"], qty_done=0)
        db.add(mp)
        # Build MO components from BOM
        bom = db.execute(select(Composition).where(Composition.produit_id == line["produit_id"]))
        for c in bom.scalars():
            qty_req = float(line["qty_to_build"]) * float(c.quantite) * (1 + float(c.dechets_pct or 0))
            db.add(MOComponent(mo_id=mo.mo_id, type_composant=c.type_composant, composant_id=c.composant_id, qty_required=qty_req, qty_issued=0))
    db.flush()
    return {"mo_id": mo.mo_id}

@router.post("/mo/{mo_id}/start")
def start_mo(mo_id: int, db: Session = Depends(get_db)):
    mo = db.get(ManufacturingOrder, mo_id)
    if not mo:
        raise HTTPException(status_code=404, detail="MO not found")
    mo.status = "in_progress"
    mo.start_time = datetime.utcnow()
    db.flush()
    return {"status": mo.status}

@router.post("/mo/{mo_id}/issue")
def issue_components(mo_id: int, payload: dict, db: Session = Depends(get_db)):
    mo = db.get(ManufacturingOrder, mo_id)
    if not mo:
        raise HTTPException(status_code=404, detail="MO not found")
    lines = payload.get("lines", [])
    for line in lines:
        # Consume components: create inventory movement '-'
        move = InventoryMovement(location_id=mo.location_id, type_item=line["type_composant"], item_id=line["composant_id"], qty=line["qty"], direction='-', motif='issue', ref_type='MO', ref_id=mo_id)
        db.add(move)
    db.flush()
    return {"issued": len(lines)}

@router.post("/mo/{mo_id}/complete")
def complete_mo(mo_id: int, db: Session = Depends(get_db)):
    mo = db.get(ManufacturingOrder, mo_id)
    if not mo:
        raise HTTPException(status_code=404, detail="MO not found")
    # Backflush components based on BOM and qty_done (simple version: use qty_to_build)
    products = db.execute(select(MOProduct).where(MOProduct.mo_id == mo_id)).scalars().all()
    for p in products:
        # receipt finished goods
        db.add(InventoryMovement(location_id=mo.location_id, type_item='produit', item_id=p.produit_id, qty=float(p.qty_to_build), direction='+', motif='receipt', ref_type='MO', ref_id=mo_id))
        # backflush components from BOM
        bom = db.execute(select(Composition).where(Composition.produit_id == p.produit_id)).scalars().all()
        for c in bom:
            qty = float(p.qty_to_build) * float(c.quantite) * (1 + float(c.dechets_pct or 0))
            db.add(InventoryMovement(location_id=mo.location_id, type_item=c.type_composant, item_id=c.composant_id, qty=qty, direction='-', motif='issue', ref_type='MO', ref_id=mo_id))
    mo.status = "done"
    mo.end_time = datetime.utcnow()
    db.flush()
    return {"status": mo.status}