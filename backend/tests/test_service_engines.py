import pytest
from app.services.service_catalogue import ServiceCatalogue, ServiceValidationResult
from app.services.discovery_service import DiscoveryService, DiscoveryRequirement, DiscoveredProvider
from app.services.ranking_service import MatchingEngine, MatchingResult
from app.models.provider import Provider

class MockCollection:
    def __init__(self, data):
        self.data = data
        
    def aggregate(self, pipeline):
        # We simply mock the aggregation return
        # Since we just want to test DiscoveryService's parsing logic
        return self.data

def test_service_catalogue_valid_service():
    cat = ServiceCatalogue()
    res = cat.validate(service="ac_repair", specialization="water_leakage")
    assert res.valid is True
    assert res.service == "ac_repair"
    assert res.specialization == "water_leakage"
    
def test_service_catalogue_invalid_specialization():
    cat = ServiceCatalogue()
    res = cat.validate(service="ac_repair", specialization="unknown_issue")
    assert res.valid is False
    assert "Unsupported specialization" in res.reason

def test_service_catalogue_normalization():
    cat = ServiceCatalogue()
    res = cat.validate(service="AC Repair", specialization="water leakage")
    assert res.valid is True
    assert res.service == "ac_repair"
    assert res.specialization == "water_leakage"

def test_discovery_engine():
    mock_db_results = [
        {
            "id": "P1",
            "name": "Test P1",
            "services": ["ac_repair"],
            "specializations": ["water_leakage"],
            "location": {"type": "Point", "coordinates": [78.4, 17.4]},
            "rating": 4.5,
            "pricing": {"min": 500, "max": 1000},
            "availability": {"status": "available", "slots": ["today"]},
            "verified": True,
            "calculated_distance": 2500
        }
    ]
    col = MockCollection(mock_db_results)
    ds = DiscoveryService(providers_col=col)
    
    req = DiscoveryRequirement(
        service="ac_repair",
        specialization="water_leakage",
        location={"lat": 17.4, "lng": 78.4},
        preferred_time="today"
    )
    
    results = ds.discover(req)
    assert len(results) == 1
    assert results[0].distance_km == 2.5
    assert results[0].provider.id == "P1"

def test_matching_engine():
    p1 = Provider(
        id="P1", name="Test P1", services=["ac_repair"], specializations=["water_leakage"],
        location={"type": "Point", "coordinates": [0,0]}, rating=5.0, pricing={"min": 500, "max": 500},
        availability={"status": "available", "slots": ["today"]}, verified=True
    )
    p2 = Provider(
        id="P2", name="Test P2", services=["ac_repair"], specializations=[], # missing specialization
        location={"type": "Point", "coordinates": [0,0]}, rating=4.0, pricing={"min": 1000, "max": 1000}, # more expensive
        availability={"status": "available", "slots": []}, verified=True # missing slot
    )
    
    dp1 = DiscoveredProvider(provider=p1, distance_km=0)
    dp2 = DiscoveredProvider(provider=p2, distance_km=50) # further away
    
    req = DiscoveryRequirement(
        service="ac_repair",
        specialization="water_leakage",
        location={"lat": 17.4, "lng": 78.4},
        preferred_time="today",
        max_distance_km=50.0
    )
    
    me = MatchingEngine()
    res = me.match(req, [dp1, dp2])
    
    assert len(res.providers) == 2
    assert res.providers[0].provider_id == "P1"
    assert res.providers[1].provider_id == "P2"
    
    p1_scores = res.providers[0].score_breakdown
    assert p1_scores.problem_compatibility == 100
    assert p1_scores.specialization == 100
    assert p1_scores.availability == 100
    assert p1_scores.distance == 100
    assert p1_scores.rating == 100
    assert p1_scores.price == 100
    assert res.providers[0].fit_score == 100.0

    p2_scores = res.providers[1].score_breakdown
    assert p2_scores.problem_compatibility == 80
    assert p2_scores.specialization == 50
    assert p2_scores.availability == 50
    assert p2_scores.distance == 0
    assert p2_scores.rating == 80
    assert p2_scores.price == 0
    
def test_matching_engine_no_candidates():
    me = MatchingEngine()
    req = DiscoveryRequirement(service="ac_repair", location={"lat": 17.4, "lng": 78.4})
    res = me.match(req, [])
    
    assert len(res.providers) == 0
    assert res.match_status == "no_match"
