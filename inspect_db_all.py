import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath('backend'))

from app.database.connection import DatabaseConnection

def main():
    client = DatabaseConnection.get_client()
    print("Databases:", client.list_database_names())
    for db_name in client.list_database_names():
        db = client[db_name]
        print(f"Collections in {db_name}:", db.list_collection_names())
        for col_name in db.list_collection_names():
            if col_name == "providers":
                print(f"Provider count in {db_name}.{col_name}:", db[col_name].count_documents({}))
                print(f"Sample doc:", db[col_name].find_one())

if __name__ == "__main__":
    main()
