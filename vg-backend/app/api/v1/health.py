from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from redis import Redis
from app.config import settings
from app.db.session import get_db

router = APIRouter()

@router.get("/health")
def healthcheck(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    r = Redis.from_url(settings.redis_url)
    r.ping()
    return {"status": "ok", "message": "auto-deploy-1"}