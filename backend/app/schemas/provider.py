from pydantic import BaseModel, Field
from typing import List, Optional
from app.models.provider import GeoJSONPoint, Pricing, Availability

class ProviderResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    services: List[str]
    specializations: List[str]
    location: GeoJSONPoint
    rating: float
    pricing: Pricing
    availability: Availability
    verified: bool
    experience: int
    service_area: str
    distance_km: Optional[float] = None

    class Config:
        populate_by_name = True

class ProviderListResponse(BaseModel):
    providers: List[ProviderResponse]
    count: int
