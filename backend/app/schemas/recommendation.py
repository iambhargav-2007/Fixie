from pydantic import BaseModel
from typing import Optional, List
from app.schemas.provider import ProviderResponse

class RequirementRequest(BaseModel):
    service: str
    specialization: Optional[str] = None
    max_distance_km: Optional[int] = 5
    minimum_rating: Optional[float] = None
    max_budget: Optional[float] = None
    preferred_time: Optional[str] = None
    preferred_date: Optional[str] = None

class LocationRequest(BaseModel):
    latitude: float
    longitude: float

class RecommendationRequest(BaseModel):
    requirements: RequirementRequest
    location: LocationRequest

class ScoreBreakdown(BaseModel):
    problem_compatibility: float
    specialization: float
    availability: float
    distance: float
    rating: float
    price: float

class RankedProviderResponse(ProviderResponse):
    rank: int
    fit_score: float
    score_breakdown: ScoreBreakdown

class RecommendationResponse(BaseModel):
    providers: List[RankedProviderResponse]
    count: int
