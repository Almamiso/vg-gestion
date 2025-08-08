from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import get_db
from app.db.models.products import Product
from app.db.models.compositions import Composition
from app.schemas.products import ProductCreate, BOMItemCreate, ProductOut

router = APIRouter()

@router.get("/products/{produit_id}", response_model=ProductOut)
def get_product(produit_id: int, db: Session = Depends(get_db)):
    product = db.get(Product, produit_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    bom_rows = db.execute(select(Composition).where(Composition.produit_id == produit_id)).scalars().all()
    bom = [BOMItemCreate(type_composant=r.type_composant, composant_id=r.composant_id, quantite=float(r.quantite), dechets_pct=float(r.dechets_pct or 0)) for r in bom_rows]
    return ProductOut(
        produit_id=product.produit_id,
        nom=product.nom,
        code=product.code,
        categorie=product.categorie,
        prix_vente=float(product.prix_vente or 0),
        actif=bool(product.actif),
        bom=bom,
    )

@router.post("/products")
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    p = Product(**payload.dict())
    db.add(p)
    db.flush()
    return {"produit_id": p.produit_id}

@router.post("/bom/{produit_id}/items")
def add_bom_items(produit_id: int, items: list[BOMItemCreate], db: Session = Depends(get_db)):
    if not db.get(Product, produit_id):
        raise HTTPException(status_code=404, detail="Product not found")
    for it in items:
        db.add(Composition(produit_id=produit_id, type_composant=it.type_composant, composant_id=it.composant_id, quantite=it.quantite, dechets_pct=it.dechets_pct))
    db.flush()
    return {"added": len(items)}