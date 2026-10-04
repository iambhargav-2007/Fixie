"""MongoDB client and connection management."""

from pymongo import MongoClient
from backend.app.config.settings import settings

class DatabaseConnection:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = MongoClient(settings.MONGODB_URI)
        return cls._client

    @classmethod
    def get_db(cls):
        client = cls.get_client()
        return client[settings.DATABASE_NAME]

def get_database():
    """Dependency for getting the database instance."""
    return DatabaseConnection.get_db()
