from fastapi import APIRouter, Query
from typing import Optional
from app.schemas.provider import ProviderListResponse, ProviderResponse
from app.services import provider_service
from app.services import discovery_service

router = APIRouter(prefix="/providers", tags=["Providers"])

@router.get("/nearby", response_model=ProviderListResponse)
def discover_nearby(
    service: str = Query(..., min_length=1),
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius: int = Query(5000, gt=0, le=25000),
    specialization: Optional[str] = None
):
    return discovery_service.discover_nearby_providers(
        service=service,
        lat=latitude,
        lon=longitude,
        radius=radius,
        specialization=specialization
    )

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
