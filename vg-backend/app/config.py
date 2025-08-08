from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    redis_url: str

    clerk_jwks_url: Optional[str] = None
    auth_audience: Optional[str] = None
    auth_issuer: Optional[str] = None
    required_role: Optional[str] = None

    shopify_api_key: Optional[str] = None
    shopify_api_secret: Optional[str] = None
    shopify_webhook_secret: Optional[str] = None
    shopify_store_us: Optional[str] = None
    shopify_store_eu: Optional[str] = None

    otel_exporter_otlp_endpoint: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

settings = Settings(
    _env_file=None  # rely on environment inside containers
)