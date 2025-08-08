import os
import httpx

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def test_health_endpoint_available():
    # This test assumes the API is running locally (via docker-compose)
    with httpx.Client(base_url=BASE_URL) as client:
        r = client.get("/api/v1/health")
        assert r.status_code == 200
        assert r.json().get("status") == "ok"