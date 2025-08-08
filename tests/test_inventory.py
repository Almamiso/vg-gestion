import os
import httpx

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def test_movement_and_transfer_flow():
    client = httpx.Client(base_url=BASE_URL)

    # Add stock +10 at location 1
    r = client.post("/api/v1/inventory/movements", json={
        "location_id": 1,
        "type_item": "produit",
        "item_id": 1,
        "qty": 10,
        "direction": "+",
        "motif": "adjust"
    })
    assert r.status_code == 200

    # Transfer 4 from 1 to 2
    r = client.post("/api/v1/inventory/transfer", json={
        "from_location_id": 1,
        "to_location_id": 2,
        "type_item": "produit",
        "item_id": 1,
        "qty": 4
    })
    assert r.status_code == 200

    # Check stock
    s1 = client.get("/api/v1/inventory/stock", params={"location_id": 1, "type_item": "produit", "item_id": 1}).json()
    s2 = client.get("/api/v1/inventory/stock", params={"location_id": 2, "type_item": "produit", "item_id": 1}).json()
    q1 = s1[0]["quantite"] if s1 else 0
    q2 = s2[0]["quantite"] if s2 else 0
    assert float(q1) == 6
    assert float(q2) == 4