import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_availability_available():
    # Example: P102 has 16:00 and 18:00
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000&preferred_time=18:00")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert p["availability"]["status"] == "available"
        assert "18:00" in p["availability"]["slots"]

def test_availability_time_mismatch():
    # If we request a time no one has, or a specific time mismatch
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000&preferred_time=20:00")
    assert response.status_code == 200
    # Assuming no one has 20:00 in seed data for AC repair nearby, or those who do are returned
    for p in response.json()["providers"]:
        assert "20:00" in p["availability"]["slots"]

def test_no_availability_requirement():
    # Should not filter by availability if not provided
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000")
    assert response.status_code == 200
    assert len(response.json()["providers"]) > 0

def test_minimum_rating():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000&minimum_rating=4.5")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert p["rating"] >= 4.5

def test_maximum_distance():
    # Handled by radius
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=2000")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert p["distance_km"] <= 2.0  # 2000m is 2.0km

def test_price_filter():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000&max_budget=700")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert p["pricing"]["min"] <= 700

def test_specialization_filter():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000&specialization=water_leakage")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert "water_leakage" in p["specializations"]

def test_combined_filters():
    response = client.get("/providers/nearby?service=ac_repair&specialization=water_leakage&latitude=17.3850&longitude=78.4867&radius=5000&minimum_rating=4.5&max_budget=700&preferred_time=18:00")
    assert response.status_code == 200
    for p in response.json()["providers"]:
        assert "ac_repair" in p["services"]
        assert "water_leakage" in p["specializations"]
        assert p["rating"] >= 4.5
        assert p["pricing"]["min"] <= 700
        assert p["availability"]["status"] == "available"
        assert "18:00" in p["availability"]["slots"]

def test_empty_results():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000&max_budget=10")
    assert response.status_code == 200
    assert response.json()["count"] == 0
    assert len(response.json()["providers"]) == 0

def test_invalid_rating():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000&minimum_rating=6")
    assert response.status_code == 422

def test_invalid_distance():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=-5")
    assert response.status_code == 422

def test_invalid_budget():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000&max_budget=-100")
    assert response.status_code == 422

def test_no_ranking_fields():
    response = client.get("/providers/nearby?service=ac_repair&latitude=17.3850&longitude=78.4867&radius=5000")
    assert response.status_code == 200
    if len(response.json()["providers"]) > 0:
        p = response.json()["providers"][0]
        assert "fit_score" not in p
        assert "rank" not in p
        assert "recommendation_score" not in p
