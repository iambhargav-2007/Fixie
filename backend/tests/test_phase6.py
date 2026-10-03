import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_request_success():
    req_data = {
        "user_id": "U101",
        "provider_id": "P1001",
        "service": "washing_machine_repair",
        "problem": {
            "issue": "not spinning"
        },
        "preferred_time": "today"
    }
    response = client.post("/requests", json=req_data)
    assert response.status_code == 201
    data = response.json()
    assert "_id" in data
    assert data["status"] == "pending"
    assert data["provider_id"] == "P1001"
    assert data["service"] == "washing_machine_repair"
    assert data["problem"]["issue"] == "not spinning"
    assert data["preferred_time"] == "today"

def test_create_request_invalid_provider():
    req_data = {
        "user_id": "U101",
        "provider_id": "NON_EXISTENT_P",
        "service": "ac_repair",
        "problem": {"issue": "test"}
    }
    response = client.post("/requests", json=req_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Provider not found"

def test_create_request_invalid_service():
    req_data = {
        "user_id": "U101",
        "provider_id": "P1001",
        "service": "plumbing", # Not offered by P1001
        "problem": {"issue": "test"}
    }
    response = client.post("/requests", json=req_data)
    assert response.status_code == 400

def test_get_requests():
    response = client.get("/requests")
    assert response.status_code == 200
    data = response.json()
    assert "requests" in data
    assert "count" in data

def test_get_request_by_id():
    req_data = {
        "user_id": "U_TEST_GET",
        "provider_id": "P1001",
        "service": "washing_machine_repair",
        "problem": {"issue": "test"}
    }
    create_resp = client.post("/requests", json=req_data)
    req_id = create_resp.json()["_id"]
    
    response = client.get(f"/requests/{req_id}")
    assert response.status_code == 200
    assert response.json()["_id"] == req_id

def test_get_request_not_found():
    response = client.get("/requests/nonexistent")
    assert response.status_code == 404

def test_status_transitions():
    req_data = {
        "user_id": "U102",
        "provider_id": "P1001",
        "service": "washing_machine_repair",
        "problem": {"issue": "test transition"}
    }
    create_resp = client.post("/requests", json=req_data)
    req_id = create_resp.json()["_id"]
    
    # pending -> accepted
    resp = client.patch(f"/requests/{req_id}/status", json={"status": "accepted"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "accepted"
    
    # accepted -> completed
    resp = client.patch(f"/requests/{req_id}/status", json={"status": "completed"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"
    
    # completed -> pending (Invalid)
    resp = client.patch(f"/requests/{req_id}/status", json={"status": "pending"})
    assert resp.status_code == 400

def test_invalid_status_value():
    req_data = {
        "user_id": "U102",
        "provider_id": "P1001",
        "service": "washing_machine_repair",
        "problem": {"issue": "test transition"}
    }
    create_resp = client.post("/requests", json=req_data)
    req_id = create_resp.json()["_id"]
    
    resp = client.patch(f"/requests/{req_id}/status", json={"status": "working"})
    assert resp.status_code == 422 # Pydantic enum validation failure

def test_request_filtering():
    # User U_TEST_FILTER
    req_data = {
        "user_id": "U_TEST_FILTER",
        "provider_id": "P1001",
        "service": "washing_machine_repair",
        "problem": {"issue": "test"}
    }
    client.post("/requests", json=req_data)
    
    response = client.get("/requests?user_id=U_TEST_FILTER")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] >= 1
    for req in data["requests"]:
        assert req["user_id"] == "U_TEST_FILTER"

def test_request_data_integrity():
    req_data = {
        "user_id": "U_INTEGRITY",
        "provider_id": "P1001",
        "service": "washing_machine_repair",
        "problem": {"issue": "issue1", "specialization": "spec1"},
        "preferred_time": "tomorrow",
        "budget": {"min": 100, "max": 200},
        "location": {"type": "Point", "coordinates": [10.0, 20.0]}
    }
    create_resp = client.post("/requests", json=req_data)
    assert create_resp.status_code == 201
    
    req_id = create_resp.json()["_id"]
    get_resp = client.get(f"/requests/{req_id}")
    assert get_resp.status_code == 200
    data = get_resp.json()
    
    assert data["user_id"] == "U_INTEGRITY"
    assert data["provider_id"] == "P1001"
    assert data["service"] == "washing_machine_repair"
    assert data["problem"]["issue"] == "issue1"
    assert data["problem"]["specialization"] == "spec1"
    assert data["preferred_time"] == "tomorrow"
    assert data["budget"]["min"] == 100
    assert data["location"]["coordinates"] == [10.0, 20.0]
