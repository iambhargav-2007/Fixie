import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_providers():
    response = client.get("/providers")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert "count" in data
    assert data["count"] > 0
    p = data["providers"][0]
    assert "_id" in p
    assert "name" in p
    assert "services" in p

def test_get_provider_by_id():
    # First get a valid ID
    providers_resp = client.get("/providers")
    provider_id = providers_resp.json()["providers"][0]["_id"]
    
    response = client.get(f"/providers/{provider_id}")
    assert response.status_code == 200
    p = response.json()
    assert p["_id"] == provider_id
    assert "name" in p
    assert "services" in p
    assert "specializations" in p
    assert "rating" in p
    assert "pricing" in p
    assert "availability" in p

def test_provider_not_found():
    response = client.get("/providers/nonexistent-provider")
    assert response.status_code == 404
    assert response.json()["detail"] == "Provider not found"

def test_nearby_providers():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    if data["count"] > 0:
        assert "distance_km" in data["providers"][0]

def test_radius_filtering():
    response_large = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=25000")
    response_small = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=1")
    assert response_large.status_code == 200
    assert response_small.status_code == 200
    assert response_large.json()["count"] >= response_small.json()["count"]
    assert response_small.json()["count"] == 0  # Likely no provider within 1 meter

def test_invalid_coordinates():
    response = client.get("/providers/nearby?service=ac_repair&latitude=100&longitude=78.4867&radius=5000")
    assert response.status_code == 422
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=200&radius=5000")
    assert response.status_code == 422

def test_invalid_radius():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=-5")
    assert response.status_code == 422

def test_empty_results():
    response = client.get("/providers/nearby?service=ac_repair&latitude=0.0&longitude=0.0&radius=5000")
    assert response.status_code == 200
    assert response.json()["count"] == 0
    assert response.json()["providers"] == []

def test_provider_data_integrity():
    response = client.get("/providers")
    p = response.json()["providers"][0]
    # Verify it doesn't have hallucinated fields like 'fit_score' which belongs to Phase 4
    assert "fit_score" not in p
    assert "rank" not in p
