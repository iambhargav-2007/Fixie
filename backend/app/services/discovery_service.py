"""Provider Discovery Engine."""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from backend.app.models.provider import Provider
from backend.app.database.collections import get_providers_collection
import logging

logger = logging.getLogger(__name__)

class DiscoveryRequirement(BaseModel):
    service: str
    specialization: Optional[str] = None
    location: Dict[str, Any]  # e.g., {"lat": 17.385, "lng": 78.486, "locality": "Hyderabad"}
    preferred_time: Optional[str] = None
    max_distance_km: float = 50.0

class DiscoveredProvider(BaseModel):
    provider: Provider
    distance_km: float

class DiscoveryService:
    def __init__(self, providers_col=None):
        self.providers_col = providers_col if providers_col is not None else get_providers_collection()

    def discover(self, req: DiscoveryRequirement) -> List[DiscoveredProvider]:
        """
        Discover eligible providers candidates using deterministic MongoDB querying.
        We filter primarily by service and location, leaving specialization and 
        availability for the Matching Engine to score and rank.
        """
        pipeline = [
            {
                "$geoNear": {
                    "near": {
                        "type": "Point",
                        "coordinates": [req.location["lng"], req.location["lat"]]
                    },
                    "distanceField": "calculated_distance",
                    "maxDistance": req.max_distance_km * 1000, # convert km to meters
                    "spherical": True,
                    "query": {
                        "services": req.service,
                        "availability.status": "available" # Must be generally available
                    }
                }
            }
        ]
        
        try:
            results = list(self.providers_col.aggregate(pipeline))
        except Exception as e:
            logger.error(f"Error executing discovery query: {e}")
            results = []
            
        discovered = []
        for doc in results:
            doc_id = doc.get("id") or str(doc.get("_id", "unknown"))
            if "_id" in doc:
                del doc["_id"]
            if "id" not in doc:
                doc["id"] = doc_id
                
            dist_km = doc.get("calculated_distance", 0) / 1000.0
            
            try:
                provider_obj = Provider(**doc)
                discovered.append(DiscoveredProvider(
                    provider=provider_obj,
                    distance_km=round(dist_km, 2)
                ))
            except Exception as e:
                logger.warning(f"Failed to parse provider document: {e}")
                
        return discovered
