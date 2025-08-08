from fastapi import APIRouter
from . import health, inventory, orders, products, manufacturing, webhooks

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(orders.router, tags=["orders"])
api_router.include_router(products.router, tags=["products"])
api_router.include_router(manufacturing.router, tags=["manufacturing"])
api_router.include_router(webhooks.router, tags=["webhooks"])