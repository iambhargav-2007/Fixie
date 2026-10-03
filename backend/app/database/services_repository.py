import re
from typing import List, Optional, Dict
from app.database.connection import get_db

def get_services(category: Optional[str] = None, search: Optional[str] = None) -> List[Dict]:
    db = get_db()
    query = {}
    if category:
        query["category"] = category
    if search:
        query["name"] = {"$regex": re.escape(search), "$options": "i"}
    
    return list(db["services"].find(query))

def get_service_by_id(service_id: str) -> Optional[Dict]:
    db = get_db()
    return db["services"].find_one({"_id": service_id})
