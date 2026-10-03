from typing import List, Optional, Dict
from app.database.connection import get_db

def get_providers(service: Optional[str] = None, specialization: Optional[str] = None, 
                  min_rating: Optional[float] = None, availability: Optional[str] = None) -> List[Dict]:
    db = get_db()
    query = {}
    
    if service:
        query["services"] = service
    if specialization:
        query["specializations"] = specialization
    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}
    if availability:
        query["availability.status"] = availability
        
    return list(db["providers"].find(query))

def get_provider_by_id(provider_id: str) -> Optional[Dict]:
    db = get_db()
    return db["providers"].find_one({"_id": provider_id})

def get_nearby_providers(
    service: str, 
    specialization: Optional[str], 
    lat: float, 
    lon: float, 
    radius_meters: int,
    minimum_rating: Optional[float] = None,
    max_budget: Optional[float] = None,
    preferred_time: Optional[str] = None,
    preferred_date: Optional[str] = None
) -> List[Dict]:
    db = get_db()
    
    query = {"services": service}
    if specialization:
        query["specializations"] = specialization
        
    if minimum_rating is not None:
        query["rating"] = {"$gte": minimum_rating}
        
    if max_budget is not None:
        query["pricing.min"] = {"$lte": max_budget}
        
    if preferred_time or preferred_date:
        query["availability.status"] = "available"
        if preferred_time:
            query["availability.slots"] = preferred_time
        
    pipeline = [
        {
            "$geoNear": {
                "near": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "distanceField": "distance_meters",
                "maxDistance": radius_meters,
                "spherical": True,
                "query": query
            }
        }
    ]
    
    return list(db["providers"].aggregate(pipeline))
