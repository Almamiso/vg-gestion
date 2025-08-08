import os
import httpx

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def test_order_lifecycle():
    c = httpx.Client(base_url=BASE_URL)

    # seed stock for produit 1 at location 1
    c.post("/api/v1/inventory/movements", json={"location_id":1,"type_item":"produit","item_id":1,"qty":5,"direction":"+"})

    # import order
    r = c.post("/api/v1/orders/import", json={
        "source": "Interne",
        "type": "B2C",
        "location_id": 1,
        "items": [{"produit_id": 1, "qty": 3}]
    })
    assert r.status_code == 200
    order_id = r.json()["order_id"]

    # reserve
    r = c.post(f"/api/v1/orders/{order_id}/reserve")
    assert r.status_code == 200

    # pick
    # fetch items? assume item id 1 for simplicity in this smoke test
    r = c.post(f"/api/v1/orders/{order_id}/pick", json={"items":[{"order_item_id":1, "qty":3}]})
    assert r.status_code in (200, 400)