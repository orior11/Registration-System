"""
MongoDB Database Connection Management
"""
from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from app.config import settings

# Global MongoDB client and database instances
_mongo_client: Optional[AsyncIOMotorClient] = None
_database = None


async def connect_to_mongo():
    """
    Connect to MongoDB database
    
    Creates an async MongoDB client and establishes connection
    """
    global _mongo_client, _database
    
    try:
        # Create async MongoDB client
        _mongo_client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            maxPoolSize=10,
            minPoolSize=1
        )
        
        # Get database reference
        _database = _mongo_client[settings.DATABASE_NAME]
        
        # Test connection
        await _mongo_client.admin.command('ping')
        
        print(f"[OK] Connected to MongoDB: {settings.DATABASE_NAME}")
        
        # Create indexes for better performance
        await _database[settings.COLLECTION_NAME].create_index("email", unique=True)
        print("[OK] Database indexes created")
        
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection
    
    Properly closes the MongoDB client connection
    """
    global _mongo_client, _database
    
    if _mongo_client:
        _mongo_client.close()
        _mongo_client = None
        _database = None
        print("[OK] MongoDB connection closed")


def get_database():
    """
    Get the current database instance
    
    Returns:
        Database instance or None if not connected
    """
    if _database is None:
        print("[WARNING] Database not initialized")
    return _database


def get_client() -> Optional[AsyncIOMotorClient]:
    """
    Get the MongoDB client instance
    
    Returns:
        MongoDB client or None if not connected
    """
    return _mongo_client
