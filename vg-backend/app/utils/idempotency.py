from __future__ import annotations
from typing import Callable, Any
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.models.webhooks import WebhookEvent


def ensure_webhook_event(db: Session, source: str, event_id: str, payload: dict) -> bool:
    existing = db.execute(
        select(WebhookEvent).where(WebhookEvent.event_id == event_id)
    ).scalar_one_or_none()
    if existing:
        return False
    db.add(WebhookEvent(source=source, event_id=event_id, payload=payload))
    db.flush()
    return True