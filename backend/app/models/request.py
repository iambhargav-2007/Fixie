from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from app.models.provider import GeoJSONPoint, Pricing

class RequestStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"
    cancelled = "cancelled"

class ProblemDescription(BaseModel):
    issue: str
    specialization: Optional[str] = None

class ServiceRequestCreate(BaseModel):
    user_id: str
    provider_id: str
    service: str
    problem: ProblemDescription
    location: Optional[GeoJSONPoint] = None
    preferred_time: Optional[str] = None
    budget: Optional[Pricing] = None

class ServiceRequestUpdateStatus(BaseModel):
    status: RequestStatus

class ServiceRequest(ServiceRequestCreate):
    id: str = Field(alias="_id")
    status: RequestStatus
    created_at: str
    updated_at: str

    class Config:
        populate_by_name = True

class ServiceRequestListResponse(BaseModel):
    requests: List[ServiceRequest]
    count: int
