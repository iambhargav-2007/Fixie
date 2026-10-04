"""Provider API routes."""

from fastapi import APIRouter, HTTPException
from backend.app.database.collections import get_providers_collection
from backend.app.models.provider import Provider
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/providers")

@router.get("/{provider_id}", response_model=Provider)
async def get_provider(provider_id: str):
    col = get_providers_collection()
    doc = col.find_one({"id": provider_id})
    
    if not doc:
        raise HTTPException(status_code=404, detail="Provider not found")
        
    if "_id" in doc:
        del doc["_id"]
        
    try:
        return Provider(**doc)
    except Exception as e:
        logger.error(f"Failed to parse provider: {e}")
        raise HTTPException(status_code=500, detail="Internal error")
