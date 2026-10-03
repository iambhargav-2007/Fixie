from pydantic import BaseModel, Field, field_validator
from typing import List

class GeoJSONPoint(BaseModel):
    type: str = "Point"
    coordinates: List[float] # [longitude, latitude]

    @field_validator('coordinates')
    @classmethod
    def validate_coords(cls, v):
        if len(v) != 2:
            raise ValueError("Coordinates must have exactly 2 elements: [longitude, latitude]")
        if not (-180 <= v[0] <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        if not (-90 <= v[1] <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return v

class Pricing(BaseModel):
    min: float
    max: float

    @field_validator('max')
    @classmethod
    def validate_pricing(cls, v, info):
        if 'min' in info.data and v < info.data['min']:
            raise ValueError("max price must be >= min price")
        return v

class Availability(BaseModel):
    status: str
    slots: List[str]

class Provider(BaseModel):
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

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, v):
        if not (0 <= v <= 5):
            raise ValueError("Rating must be between 0 and 5")
        return v

    @field_validator('services')
    @classmethod
    def validate_services(cls, v):
        if not v:
            raise ValueError("Services list cannot be empty")
        return v

    class Config:
        populate_by_name = True
