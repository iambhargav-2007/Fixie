from typing import Optional
from app.database import services_repository
from app.schemas.service import ServiceListResponse, ServiceResponse
from fastapi import HTTPException

def list_services(category: Optional[str] = None, search: Optional[str] = None) -> ServiceListResponse:
    services_data = services_repository.get_services(category, search)
    services = [ServiceResponse(**s) for s in services_data]
    return ServiceListResponse(services=services, count=len(services))

def get_service(service_id: str) -> ServiceResponse:
    service_data = services_repository.get_service_by_id(service_id)
    if not service_data:
        raise HTTPException(status_code=404, detail=f"Service {service_id} not found")
    return ServiceResponse(**service_data)
