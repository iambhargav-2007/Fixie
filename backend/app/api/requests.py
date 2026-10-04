"""Service Request API routes."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import uuid
import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/requests")

# In-memory store for hackathon prototype
_requests = {}

class ServiceRequestInput(BaseModel):
    provider_id: str
    problem: Dict[str, Any]
    service: Dict[str, str]
    location: Dict[str, Any]
    preferred_time: Optional[str] = None

class ServiceRequestStatusUpdate(BaseModel):
    status: str

@router.post("")
async def create_request(req: ServiceRequestInput):
    request_id = f"req-{uuid.uuid4().hex[:8]}"
    
    _requests[request_id] = {
        "id": request_id,
        "provider_id": req.provider_id,
        "problem": req.problem,
        "service": req.service,
        "location": req.location,
        "preferred_time": req.preferred_time,
        "status": "pending",
        "created_at": datetime.datetime.now().isoformat()
    }
    
    return _requests[request_id]

@router.get("")
async def list_requests():
    return list(_requests.values())

@router.get("/{request_id}")
async def get_request(request_id: str):
    if request_id not in _requests:
        raise HTTPException(status_code=404, detail="Request not found")
    return _requests[request_id]

@router.post("/{request_id}/accept")
async def accept_request(request_id: str):
    if request_id not in _requests:
        raise HTTPException(status_code=404, detail="Request not found")
        
    _requests[request_id]["status"] = "accepted"
    _requests[request_id]["updated_at"] = datetime.datetime.now().isoformat()
    
    return _requests[request_id]

@router.post("/{request_id}/status")
async def update_request_status(request_id: str, update: ServiceRequestStatusUpdate):
    if request_id not in _requests:
        raise HTTPException(status_code=404, detail="Request not found")
        
    _requests[request_id]["status"] = update.status
    _requests[request_id]["updated_at"] = datetime.datetime.now().isoformat()
    
    return _requests[request_id]
