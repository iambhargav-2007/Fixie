import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_nearby_missing_params():
    response = client.get("/providers/nearby")
    assert response.status_code == 422
    
def test_nearby_invalid_latitude():
    response = client.get("/providers/nearby?service=ac_repair&latitude=100&longitude=78.4867&radius=5000")
    assert response.status_code == 422

def test_nearby_invalid_longitude():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=200&radius=5000")
    assert response.status_code == 422

def test_nearby_invalid_radius():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=-5000")
    assert response.status_code == 422
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=30000")
    assert response.status_code == 422

def test_nearby_unknown_service():
    response = client.get("/providers/nearby?service=unknown_service&latitude=17.3850&longitude=78.4867&radius=5000")
    assert response.status_code == 400
    assert "Unknown service" in response.json()["detail"]

def test_nearby_valid_search():
    # Example test using a default location in Hyderabad
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    for p in data["providers"]:
        assert "ac_repair" in p["services"]
        assert "distance_km" in p
        assert p["distance_km"] >= 0

def test_nearby_specialization():
    response = client.get("/providers/nearby?service=ac_repair&specialization=water_leakage&latitude=17.3850&longitude=78.4867&radius=5000")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert "water_leakage" in p["specializations"]

def test_nearby_no_results():
    # Very remote location where no providers should exist
    response = client.get("/providers/nearby?service=ac_repair&latitude=0.0&longitude=0.0&radius=5000")
    assert response.status_code == 200
    assert response.json()["count"] == 0
    assert len(response.json()["providers"]) == 0
