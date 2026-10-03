"""Service request data models and schemas."""

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class ServiceRequestCreate(BaseModel):
    """Schema for creating a service request."""
    provider_id: str
    service: str
    problem: Dict[str, Any] = Field(default_factory=dict)
    preferred_time: Optional[str] = None


class ServiceRequest(BaseModel):
    """Schema for a confirmed or stored service request."""
    id: str
    provider_id: str
    service: str
    problem: Dict[str, Any]
    preferred_time: Optional[str] = None
    status: str = "pending"
    created_at: Optional[str] = None
