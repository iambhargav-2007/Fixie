"""
Seed the MongoDB database with providers from seed/providers.json.
Run from the project root:  python seed_db.py
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))

from backend.app.config.settings import settings
from backend.app.database.connection import DatabaseConnection
from pymongo import GEOSPHERE

def seed():
    db = DatabaseConnection.get_db()
    providers_col = db["providers"]

    # Load seed data
    seed_path = os.path.join(os.path.dirname(__file__), "seed", "providers.json")
    with open(seed_path, "r") as f:
        providers = json.load(f)

    print(f"Loaded {len(providers)} providers from seed file.")

    # Wipe old data
    deleted = providers_col.delete_many({})
    print(f"Deleted {deleted.deleted_count} old provider documents.")

    # Insert fresh data
    result = providers_col.insert_many(providers)
    print(f"Inserted {len(result.inserted_ids)} providers.")

    # Ensure geospatial index exists
    existing = providers_col.index_information()
    has_geo = any("2dsphere" in str(v.get("key")) for v in existing.values())
    if not has_geo:
        providers_col.create_index([("location", GEOSPHERE)])
        print("Created 2dsphere index on 'location'.")
    else:
        print("Geospatial index already exists.")

    # Verify
    count = providers_col.count_documents({})
    sample = providers_col.find_one({}, {"_id": 0, "id": 1, "name": 1, "services": 1})
    print(f"\nVerification: {count} providers in DB. Sample: {sample}")
    print("\nSeeding complete!")

if __name__ == "__main__":
    seed()
