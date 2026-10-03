from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.provider import ProviderListResponse, ProviderResponse
from app.services import provider_service

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.get("", response_model=ProviderListResponse)
def get_providers(
    service: Optional[str] = None,
    specialization: Optional[str] = None,
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    availability: Optional[str] = Query(None, pattern="^(available|unavailable)$")
):
    return provider_service.list_providers(service, specialization, min_rating, availability)

@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: str):
    return provider_service.get_provider(provider_id)
