"""MongoDB collection definitions and geospatial index schemas."""

from pymongo import GEOSPHERE
from backend.app.database.connection import get_database

PROVIDERS_COLLECTION = "providers"
SERVICES_COLLECTION = "services"

def get_providers_collection():
    db = get_database()
    return db[PROVIDERS_COLLECTION]

def get_services_collection():
    db = get_database()
    return db[SERVICES_COLLECTION]

def verify_indexes():
    """Verify and create necessary indexes on collections."""
    providers = get_providers_collection()
    
    # Check if 2dsphere index exists on 'location'
    existing_indexes = providers.index_information()
    index_exists = any(
        idx.get('key') == [('location', '2dsphere')]
        for name, idx in existing_indexes.items()
    )
    
    if not index_exists:
        providers.create_index([("location", GEOSPHERE)])
