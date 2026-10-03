"""Provider data models and schemas."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class GeoJSONPoint(BaseModel):
    """GeoJSON Point geometry schema for geospatial queries."""
    type: str = "Point"
    coordinates: List[float] = Field(..., description="[longitude, latitude]")


class PricingRange(BaseModel):
    """Provider estimated pricing range."""
    min: float
    max: float


class Availability(BaseModel):
    """Provider availability status and open slots."""
    status: str
    slots: List[str] = []


class Provider(BaseModel):
    """Service provider entity schema."""
    id: str
    name: str
    services: List[str] = []
    specializations: List[str] = []
    location: GeoJSONPoint
    rating: float = 0.0
    pricing: PricingRange
    availability: Availability
    verified: bool = False
