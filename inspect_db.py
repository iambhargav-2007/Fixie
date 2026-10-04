import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath('backend'))

from app.database.connection import get_database
from app.database.collections import get_providers_collection, verify_indexes

def main():
    verify_indexes()
    col = get_providers_collection()
    print("Provider count:", col.count_documents({}))
    doc = col.find_one()
    print("Sample doc:", doc)

if __name__ == "__main__":
    main()
