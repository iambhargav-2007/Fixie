import sys
import os
import random
import uuid

# Add the root project directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.app.database.collections import get_providers_collection

# 10 prominent areas in Hyderabad
AREAS = [
    {"name": "Madhapur", "lat": 17.4483, "lng": 78.3915},
    {"name": "Gachibowli", "lat": 17.4401, "lng": 78.3489},
    {"name": "Jubilee Hills", "lat": 17.4326, "lng": 78.4071},
    {"name": "Banjara Hills", "lat": 17.4156, "lng": 78.4347},
    {"name": "Secunderabad", "lat": 17.4399, "lng": 78.4983},
    {"name": "Kukatpally", "lat": 17.4933, "lng": 78.3992},
    {"name": "L.B. Nagar", "lat": 17.3457, "lng": 78.5522},
    {"name": "Uppal", "lat": 17.4018, "lng": 78.5602},
    {"name": "Mehdipatnam", "lat": 17.3916, "lng": 78.4300},
    {"name": "Dilsukhnagar", "lat": 17.3688, "lng": 78.5247}
]

# The 6 broad service categories and their underlying service IDs
CATEGORIES = [
    {
        "category": "Appliance Repair",
        "services": ["ac_repair", "ac_cleaning", "washing_machine_repair", "refrigerator_repair", "tv_repair"],
        "specializations": ["water_leakage", "not_cooling", "drum_not_spinning", "compressor_noise", "no_display"]
    },
    {
        "category": "Plumbing",
        "services": ["pipe_leakage", "tap_repair", "drainage_blockage"],
        "specializations": ["water_dripping", "pipe_crack", "continuous_drip", "clogged_sewer"]
    },
    {
        "category": "Electrical",
        "services": ["fan_repair", "switch_repair", "wiring_repair"],
        "specializations": ["short_circuit", "sparking", "abnormal_noise", "frequent_tripping"]
    },
    {
        "category": "Home Maintenance",
        "services": ["painting", "furniture_repair", "wall_repair"],
        "specializations": ["peeling_paint", "door_misalignment", "cracks", "water_seepage"]
    },
    {
        "category": "Vehicle Assistance",
        "services": ["battery_assistance", "tyre_assistance", "minor_breakdown"],
        "specializations": ["dead_battery", "flat_tyre", "engine_overheating"]
    },
    {
        "category": "Cleaning",
        "services": ["home_cleaning", "sofa_cleaning"],
        "specializations": ["deep_stains", "move_in_cleaning", "dust_mites"]
    }
]

def generate_providers():
    col = get_providers_collection()
    
    new_providers = []
    
    # We want varied ratings
    rating_pool = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 4.8, 5.0]
    
    for area in AREAS:
        # Generate 1-2 providers per category in this area (around 6-12 total per area)
        for cat in CATEGORIES:
            num_providers = random.randint(1, 2)
            for _ in range(num_providers):
                # Randomize location slightly around the area center
                lat_jitter = random.uniform(-0.02, 0.02)
                lng_jitter = random.uniform(-0.02, 0.02)
                
                provider_id = f"P_{uuid.uuid4().hex[:8]}"
                provider_name = f"{area['name']} {cat['category']} Pros {random.randint(10, 99)}"
                
                # Assign 1 to 3 random services from this category
                k_services = min(len(cat["services"]), random.randint(1, 3))
                assigned_services = random.sample(cat["services"], k_services)
                
                # Assign 1 to 3 random specializations
                k_specs = min(len(cat["specializations"]), random.randint(1, 3))
                assigned_specs = random.sample(cat["specializations"], k_specs)
                
                rating = random.choice(rating_pool)
                
                new_providers.append({
                    "id": provider_id,
                    "name": provider_name,
                    "services": assigned_services,
                    "specializations": assigned_specs,
                    "location": {
                        "type": "Point",
                        "coordinates": [area["lng"] + lng_jitter, area["lat"] + lat_jitter]
                    },
                    "rating": rating,
                    "pricing": {
                        "min": random.randint(100, 500),
                        "max": random.randint(600, 2000)
                    },
                    "availability": {
                        "status": "available" if random.random() > 0.1 else "busy",
                        "slots": ["today_immediate", "today_evening", "tomorrow_morning"]
                    },
                    "verified": random.choice([True, False])
                })

    # Create 2dsphere index if not exists
    col.create_index([("location", "2dsphere")])
    
    inserted = 0
    for p in new_providers:
        res = col.update_one({"id": p["id"]}, {"$set": p}, upsert=True)
        if res.upserted_id or res.modified_count:
            inserted += 1
            
    print(f"Successfully seeded {len(new_providers)} diverse providers across {len(AREAS)} areas in Hyderabad.")

if __name__ == "__main__":
    generate_providers()
