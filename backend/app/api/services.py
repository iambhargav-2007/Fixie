from fastapi import APIRouter
from typing import Optional
from app.schemas.service import ServiceListResponse, ServiceResponse
from app.services import service_catalogue

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("", response_model=ServiceListResponse)
def get_services(category: Optional[str] = None, search: Optional[str] = None):
    return service_catalogue.list_services(category, search)

@router.get("/{service_id}", response_model=ServiceResponse)
def get_service(service_id: str):
    return service_catalogue.get_service(service_id)
