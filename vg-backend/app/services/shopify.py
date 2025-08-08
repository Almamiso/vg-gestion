import hmac
import hashlib
import base64
from app.config import settings

HEADER_HMAC = "X-Shopify-Hmac-Sha256"
HEADER_TOPIC = "X-Shopify-Topic"
HEADER_WEBHOOK_ID = "X-Shopify-Webhook-Id"
HEADER_SHOP_DOMAIN = "X-Shopify-Shop-Domain"


def verify_hmac(body: bytes, header_hmac: str | None) -> bool:
    secret = (settings.shopify_webhook_secret or "").encode()
    mac = hmac.new(secret, body, hashlib.sha256).digest()
    calc = base64.b64encode(mac).decode()
    if not header_hmac:
        return False
    try:
        return hmac.compare_digest(calc, header_hmac)
    except Exception:
        return False