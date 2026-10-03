import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "fixfind_db")

def get_db():
    try:
        if MONGODB_URI:
            client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            # Verify connection
            client.admin.command('ping')
            db = client[DATABASE_NAME]
            return db
        else:
            print("MONGODB_URI environment variable not set")
            return None
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return None

db = get_db()
