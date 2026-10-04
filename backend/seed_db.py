import sys
import os

# Add the root project directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.app.database.collections import get_providers_collection

def seed_providers():
    col = get_providers_collection()
    
    new_providers = [
        {
            "id": "P108",
            "name": "Gandimaisamma AC Experts",
            "services": ["ac_repair", "ac_installation", "ac_cleaning"],
            "specializations": ["water_leakage", "gas_charging", "compressor_issues"],
            "location": {
                "type": "Point",
                "coordinates": [78.4116, 17.5878] # Gandimaisamma
            },
            "rating": 4.9,
            "pricing": {
                "min": 500,
                "max": 1200
            },
            "availability": {
                "status": "available",
                "slots": ["today_immediate", "today_evening"]
            },
            "verified": True
        },
        {
            "id": "P109",
            "name": "Quick Fix AC Repair Medchal",
            "services": ["ac_repair", "appliance_repair"],
            "specializations": ["water_leakage", "pcb_repair"],
            "location": {
                "type": "Point",
                "coordinates": [78.4800, 17.6200] # Near Medchal/Gandimaisamma
            },
            "rating": 4.6,
            "pricing": {
                "min": 400,
                "max": 900
            },
            "availability": {
                "status": "available",
                "slots": ["tomorrow_morning"]
            },
            "verified": True
        },
        {
            "id": "P110",
            "name": "Kompally Coolers",
            "services": ["ac_repair", "refrigerator_repair"],
            "specializations": ["cooling_failure", "water_leakage"],
            "location": {
                "type": "Point",
                "coordinates": [78.4849, 17.5348] # Kompally
            },
            "rating": 4.8,
            "pricing": {
                "min": 350,
                "max": 800
            },
            "availability": {
                "status": "available",
                "slots": ["today_afternoon", "tomorrow_morning"]
            },
            "verified": True
        }
    ]
    
    # Create 2dsphere index if not exists
    col.create_index([("location", "2dsphere")])
    
    inserted = 0
    for p in new_providers:
        # Upsert based on provider ID to avoid duplicates
        res = col.update_one({"id": p["id"]}, {"$set": p}, upsert=True)
        if res.upserted_id or res.modified_count:
            inserted += 1
            
    print(f"Successfully seeded {inserted} providers near Gandimaisamma/Hyderabad.")

if __name__ == "__main__":
    seed_providers()
