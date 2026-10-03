from fastapi import APIRouter, Query, Path, Body
from typing import Optional
from app.models.request import ServiceRequest, ServiceRequestCreate, ServiceRequestListResponse, ServiceRequestUpdateStatus
from app.services import request_service

router = APIRouter(prefix="/requests", tags=["Requests"])

@router.post("", response_model=ServiceRequest, status_code=201)
def create_request(request_in: ServiceRequestCreate):
    return request_service.create_request(request_in)

@router.get("", response_model=ServiceRequestListResponse)
def get_requests(
    user_id: Optional[str] = None,
    provider_id: Optional[str] = None,
    status: Optional[str] = None
):
    return request_service.get_requests(user_id=user_id, provider_id=provider_id, status=status)

@router.get("/{request_id}", response_model=ServiceRequest)
def get_request(request_id: str):
    return request_service.get_request_by_id(request_id)

@router.patch("/{request_id}/status", response_model=ServiceRequest)
def update_request_status(
    request_id: str,
    status_update: ServiceRequestUpdateStatus
):
    return request_service.update_request_status(request_id, status_update.status)
