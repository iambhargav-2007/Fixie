import json
import os
from pydantic import ValidationError
from app.database.connection import get_db
from app.models.provider import Provider
from app.models.service import Service

def seed_database():
    db = get_db()
    if db is None:
        print("Database connection failed. Exiting seed.")
        return

    seed_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "seed")
    services_path = os.path.join(seed_dir, "services.json")
    providers_path = os.path.join(seed_dir, "providers.json")

    # Load and validate services
    with open(services_path, 'r') as f:
        services_data = json.load(f)
    
    valid_services = []
    service_ids = set()
    for s_data in services_data:
        try:
            s = Service(**s_data)
            valid_services.append(s.model_dump(by_alias=True))
            service_ids.add(s.service_id)
        except ValidationError as e:
            print(f"Service validation failed for {s_data.get('_id')}: {e}")
            return

    # Load and validate providers
    with open(providers_path, 'r') as f:
        providers_data = json.load(f)

    valid_providers = []
    for p_data in providers_data:
        # Check referenced service IDs
        for sid in p_data.get('services', []):
            if sid not in service_ids:
                print(f"Provider {p_data.get('_id')} references invalid service: {sid}")
                return
        try:
            p = Provider(**p_data)
            valid_providers.append(p.model_dump(by_alias=True))
        except ValidationError as e:
            print(f"Provider validation failed for {p_data.get('_id')}: {e}")
            return

    # Upsert services
    services_collection = db['services']
    for s in valid_services:
        services_collection.update_one({'_id': s['_id']}, {'$set': s}, upsert=True)

    # Upsert providers
    providers_collection = db['providers']
    for p in valid_providers:
        providers_collection.update_one({'_id': p['_id']}, {'$set': p}, upsert=True)

    print(f"Connected to MongoDB")
    print(f"Services: {len(valid_services)}")
    print(f"Providers: {len(valid_providers)}")
    print("\nSeeding completed successfully.")

if __name__ == "__main__":
    seed_database()
