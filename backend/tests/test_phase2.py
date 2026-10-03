import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_services():
    response = client.get("/services")
    assert response.status_code == 200
    data = response.json()
    assert "services" in data
    assert "count" in data
    assert data["count"] > 0

def test_get_service_valid():
    response = client.get("/services/ac_repair")
    assert response.status_code == 200
    assert response.json()["_id"] == "ac_repair"

def test_get_service_invalid():
    response = client.get("/services/invalid-id")
    assert response.status_code == 404

def test_service_filtering_category():
    response = client.get("/services?category=appliance_repair")
    assert response.status_code == 200
    for s in response.json()["services"]:
        assert s["category"] == "appliance_repair"

def test_service_filtering_search():
    response = client.get("/services?search=AC")
    assert response.status_code == 200
    assert len(response.json()["services"]) > 0
    for s in response.json()["services"]:
        assert "ac" in s["name"].lower()

def test_get_providers():
    response = client.get("/providers")
    assert response.status_code == 200
    data = response.json()
    assert "providers" in data
    assert "count" in data
    assert data["count"] > 0

def test_get_provider_invalid():
    response = client.get("/providers/invalid-id")
    assert response.status_code == 404

def test_provider_filtering_service():
    response = client.get("/providers?service=ac_repair")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert "ac_repair" in p["services"]

def test_provider_filtering_specialization():
    response = client.get("/providers?specialization=general")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert "general" in p["specializations"]

def test_provider_filtering_rating():
    response = client.get("/providers?min_rating=4.5")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert p["rating"] >= 4.5

def test_provider_filtering_availability():
    response = client.get("/providers?availability=available")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert p["availability"]["status"] == "available"

def test_provider_filtering_combined():
    response = client.get("/providers?service=ac_repair&min_rating=4.5&availability=available")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert "ac_repair" in p["services"]
        assert p["rating"] >= 4.5
        assert p["availability"]["status"] == "available"

def test_provider_invalid_rating():
    response = client.get("/providers?min_rating=10")
    assert response.status_code == 422
    response = client.get("/providers?min_rating=-1")
    assert response.status_code == 422

def test_provider_invalid_availability():
    response = client.get("/providers?availability=invalid_status")
    assert response.status_code == 422
