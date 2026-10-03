from datetime import datetime, timezone
import uuid
from typing import List, Optional, Dict, Any
from app.database.connection import get_db

def _get_collection():
    return get_db()["service_requests"]

def create_request(data: dict) -> dict:
    req_id = f"REQ{uuid.uuid4().hex[:8].upper()}"
    now = datetime.now(timezone.utc).isoformat()
    data["_id"] = req_id
    data["status"] = "pending"
    data["created_at"] = now
    data["updated_at"] = now
    _get_collection().insert_one(data)
    return get_request_by_id(req_id)

def get_request_by_id(request_id: str) -> Optional[dict]:
    return _get_collection().find_one({"_id": request_id})

def get_requests(user_id: Optional[str] = None, provider_id: Optional[str] = None, status: Optional[str] = None) -> List[dict]:
    query = {}
    if user_id:
        query["user_id"] = user_id
    if provider_id:
        query["provider_id"] = provider_id
    if status:
        query["status"] = status
    cursor = _get_collection().find(query).sort("created_at", -1)
    return list(cursor)

def update_request_status(request_id: str, new_status: str) -> Optional[dict]:
    now = datetime.now(timezone.utc).isoformat()
    from pymongo import ReturnDocument
    result = _get_collection().find_one_and_update(
        {"_id": request_id},
        {"$set": {"status": new_status, "updated_at": now}},
        return_document=ReturnDocument.AFTER
    )
    return result
