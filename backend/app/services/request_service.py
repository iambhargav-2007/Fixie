from fastapi import HTTPException
from app.models.request import ServiceRequestCreate, ServiceRequest, RequestStatus, ServiceRequestListResponse
from app.database import requests_repository, providers_repository

def create_request(request_in: ServiceRequestCreate) -> ServiceRequest:
    # 1. Validate Provider exists
    provider_data = providers_repository.get_provider_by_id(request_in.provider_id)
    if not provider_data:
        raise HTTPException(status_code=404, detail="Provider not found")
        
    # 2. Validate Service exists for provider
    if request_in.service not in provider_data.get("services", []):
        raise HTTPException(status_code=400, detail="Provider does not offer this service")
        
    data = request_in.model_dump(exclude_unset=True)
    
    # Store request
    new_req = requests_repository.create_request(data)
    return ServiceRequest(**new_req)

def get_requests(user_id: str = None, provider_id: str = None, status: str = None) -> ServiceRequestListResponse:
    requests = requests_repository.get_requests(user_id=user_id, provider_id=provider_id, status=status)
    req_models = [ServiceRequest(**r) for r in requests]
    return ServiceRequestListResponse(requests=req_models, count=len(req_models))

def get_request_by_id(request_id: str) -> ServiceRequest:
    req = requests_repository.get_request_by_id(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return ServiceRequest(**req)

VALID_TRANSITIONS = {
    RequestStatus.pending: [RequestStatus.accepted, RequestStatus.rejected, RequestStatus.cancelled],
    RequestStatus.accepted: [RequestStatus.completed, RequestStatus.cancelled],
    RequestStatus.rejected: [],
    RequestStatus.completed: [],
    RequestStatus.cancelled: []
}

def update_request_status(request_id: str, new_status: RequestStatus) -> ServiceRequest:
    req = requests_repository.get_request_by_id(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
        
    current_status = RequestStatus(req["status"])
    if new_status not in VALID_TRANSITIONS[current_status]:
        raise HTTPException(status_code=400, detail=f"Invalid transition from {current_status.value} to {new_status.value}")
        
    updated_req = requests_repository.update_request_status(request_id, new_status.value)
    return ServiceRequest(**updated_req)
