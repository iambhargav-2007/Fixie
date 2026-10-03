from typing import Optional
from app.database import providers_repository
from app.schemas.provider import ProviderListResponse, ProviderResponse
from fastapi import HTTPException

def list_providers(service: Optional[str] = None, specialization: Optional[str] = None, 
                   min_rating: Optional[float] = None, availability: Optional[str] = None) -> ProviderListResponse:
    providers_data = providers_repository.get_providers(service, specialization, min_rating, availability)
    providers = [ProviderResponse(**p) for p in providers_data]
    return ProviderListResponse(providers=providers, count=len(providers))

def get_provider(provider_id: str) -> ProviderResponse:
    provider_data = providers_repository.get_provider_by_id(provider_id)
    if not provider_data:
        raise HTTPException(status_code=404, detail="Provider not found")
    return ProviderResponse(**provider_data)
