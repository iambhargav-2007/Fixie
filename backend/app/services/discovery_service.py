from typing import Optional
from fastapi import HTTPException
from app.database import providers_repository
from app.database import services_repository
from app.schemas.provider import ProviderListResponse, ProviderResponse

def discover_nearby_providers(
    service: str,
    lat: float,
    lon: float,
    radius: int,
    specialization: Optional[str] = None
) -> ProviderListResponse:
    # Validate service exists
    svc = services_repository.get_service_by_id(service)
    if not svc:
        raise HTTPException(status_code=400, detail=f"Unknown service: {service}")
        
    providers_data = providers_repository.get_nearby_providers(
        service=service,
        specialization=specialization,
        lat=lat,
        lon=lon,
        radius_meters=radius
    )
    
    providers = []
    for p in providers_data:
        dist_m = p.get("distance_meters", 0)
        p["distance_km"] = round(dist_m / 1000.0, 2)
        providers.append(ProviderResponse(**p))
        
    return ProviderListResponse(providers=providers, count=len(providers))
