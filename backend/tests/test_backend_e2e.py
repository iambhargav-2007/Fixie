import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_backend_flow():
    # 1-6: Discovery, Filtering, Ranking
    # Use the /recommendations endpoint to perform the full deterministic flow
    rec_payload = {
        "requirements": {
            "service": "ac_repair",
            "specialization": "water_leakage",
            "max_distance_km": 15,
            "minimum_rating": 4.0
        },
        "location": {
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    }
    rec_resp = client.post("/recommendations", json=rec_payload)
    assert rec_resp.status_code == 200
    rec_data = rec_resp.json()
    assert rec_data["count"] > 0
    
    # 7. Select a provider
    ranked_providers = rec_data["providers"]
    top_provider = ranked_providers[0]
    provider_id = top_provider["_id"] if "_id" in top_provider else top_provider["id"]
    
    assert top_provider["rank"] == 1
    assert top_provider["fit_score"] > 0
    
    # 8. Create service request
    req_payload = {
        "user_id": "U_E2E_TESTER",
        "provider_id": provider_id,
        "service": "ac_repair",
        "problem": {
            "issue": "water_leakage",
            "specialization": "drainage"
        },
        "preferred_time": "today",
        "location": {
            "type": "Point",
            "coordinates": [78.4867, 17.3850]
        }
    }
    
    create_resp = client.post("/requests", json=req_payload)
    assert create_resp.status_code == 201
    created_req = create_resp.json()
    
    # 9. Verify pending status
    req_id = created_req["_id"] if "_id" in created_req else created_req["id"]
    assert created_req["status"] == "pending"
    
    # 10. Retrieve request
    get_resp = client.get(f"/requests/{req_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["status"] == "pending"
    
    # 11. Change status to accepted
    patch_accept = client.patch(f"/requests/{req_id}/status", json={"status": "accepted"})
    assert patch_accept.status_code == 200
    assert patch_accept.json()["status"] == "accepted"
    
    # 12. Verify persistence
    get_resp2 = client.get(f"/requests/{req_id}")
    assert get_resp2.status_code == 200
    assert get_resp2.json()["status"] == "accepted"
    
    # 13. Change status to completed
    patch_complete = client.patch(f"/requests/{req_id}/status", json={"status": "completed"})
    assert patch_complete.status_code == 200
    assert patch_complete.json()["status"] == "completed"
    
    # 14. Verify final persistence
    get_resp3 = client.get(f"/requests/{req_id}")
    assert get_resp3.status_code == 200
    assert get_resp3.json()["status"] == "completed"

def test_washing_machine_scenario():
    # 22. Secondary demo flow
    rec_payload = {
        "requirements": {
            "service": "washing_machine_repair",
            "max_distance_km": 15
        },
        "location": {
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    }
    rec_resp = client.post("/recommendations", json=rec_payload)
    assert rec_resp.status_code == 200
    
    rec_data = rec_resp.json()
    assert rec_data["count"] > 0
    top_provider = rec_data["providers"][0]
    
    # Verify the chosen provider actually supports the service
    assert "washing_machine_repair" in top_provider["services"]
        
def test_no_provider_scenario():
    # 23. No provider scenario
    rec_payload = {
        "requirements": {
            "service": "ac_repair",
            "minimum_rating": 10.0,
            "max_distance_km": 15
        },
        "location": {
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    }
    rec_resp = client.post("/recommendations", json=rec_payload)
    assert rec_resp.status_code == 200
    assert rec_resp.json()["count"] == 0
    assert rec_resp.json()["providers"] == []
