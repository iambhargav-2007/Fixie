import pytest
from app.models.provider import Provider, GeoJSONPoint, Pricing, Availability
from app.models.service import Service
from pydantic import ValidationError

def test_service_validation():
    data = {
        "_id": "ac_repair",
        "category": "appliance_repair",
        "name": "AC Repair",
        "specializations": ["water_leakage"]
    }
    s = Service(**data)
    assert s.service_id == "ac_repair"

def test_provider_validation_success():
    data = {
        "_id": "P1001",
        "name": "Test Provider",
        "services": ["ac_repair"],
        "specializations": ["general"],
        "location": {
            "type": "Point",
            "coordinates": [78.4867, 17.3850]
        },
        "rating": 4.5,
        "pricing": {
            "min": 100,
            "max": 500
        },
        "availability": {
            "status": "available",
            "slots": ["10:00"]
        },
        "verified": True,
        "experience": 5,
        "service_area": "Hyderabad"
    }
    p = Provider(**data)
    assert p.id == "P1001"
    assert p.location.coordinates == [78.4867, 17.3850]

def test_provider_invalid_rating():
    data = {
        "_id": "P1001",
        "name": "Test Provider",
        "services": ["ac_repair"],
        "specializations": ["general"],
        "location": {"type": "Point", "coordinates": [78.0, 17.0]},
        "rating": 6.0,
        "pricing": {"min": 100, "max": 500},
        "availability": {"status": "available", "slots": []},
        "verified": True,
        "experience": 5,
        "service_area": "Hyderabad"
    }
    with pytest.raises(ValidationError):
        Provider(**data)

def test_provider_invalid_pricing():
    data = {
        "_id": "P1001",
        "name": "Test Provider",
        "services": ["ac_repair"],
        "specializations": ["general"],
        "location": {"type": "Point", "coordinates": [78.0, 17.0]},
        "rating": 4.0,
        "pricing": {"min": 500, "max": 100},
        "availability": {"status": "available", "slots": []},
        "verified": True,
        "experience": 5,
        "service_area": "Hyderabad"
    }
    with pytest.raises(ValidationError):
        Provider(**data)

def test_provider_invalid_coordinates():
    data = {
        "_id": "P1001",
        "name": "Test Provider",
        "services": ["ac_repair"],
        "specializations": ["general"],
        "location": {"type": "Point", "coordinates": [78.0, 17.0, 1.0]},
        "rating": 4.0,
        "pricing": {"min": 100, "max": 500},
        "availability": {"status": "available", "slots": []},
        "verified": True,
        "experience": 5,
        "service_area": "Hyderabad"
    }
    with pytest.raises(ValidationError):
        Provider(**data)
