"""
User Service - CRUD operations for user management
"""
from typing import Optional, Dict
from datetime import datetime, timedelta
from bson import ObjectId
from app.database import get_database
from app.config import settings
from app.auth.password import hash_password


async def get_user_by_email(email: str) -> Optional[Dict]:
    """
    Get user by email address
    
    Args:
        email: User's email address
        
    Returns:
        User document or None if not found
    """
    db = get_database()
    if db is None:
        return None
    
    user = await db[settings.COLLECTION_NAME].find_one({"email": email.lower()})
    return user


async def get_user_by_id(user_id: str) -> Optional[Dict]:
    """
    Get user by ID
    
    Args:
        user_id: User's MongoDB ObjectId as string
        
    Returns:
        User document or None if not found
    """
    db = get_database()
    if db is None:
        return None
    
    try:
        user = await db[settings.COLLECTION_NAME].find_one({"_id": ObjectId(user_id)})
        return user
    except Exception:
        return None


async def create_user(name: str, email: str, password: str) -> Optional[str]:
    """
    Create a new user
    
    Args:
        name: User's full name
        email: User's email address
        password: User's plain text password (will be hashed)
        
    Returns:
        User ID as string or None if creation failed
    """
    db = get_database()
    if db is None:
        return None
    
    password_hash = hash_password(password)
    
    user_doc = {
        "name": name,
        "email": email.lower(),
        "password_hash": password_hash,
        "social_provider": None,
        "social_provider_id": None,
        "created_at": datetime.utcnow(),
        "last_login": None,
        "is_verified": False,
        "reset_code": None,
        "reset_code_expires": None
    }
    
    try:
        result = await db[settings.COLLECTION_NAME].insert_one(user_doc)
        return str(result.inserted_id)
    except Exception as e:
        print(f"[ERROR] Error creating user: {e}")
        return None


async def create_social_user(name: str, email: str, provider: str, provider_id: str) -> Optional[str]:
    """
    Create a new user from social login (Google, Facebook, etc.)
    
    Args:
        name: User's full name
        email: User's email address
        provider: Social provider name (google, facebook)
        provider_id: User's ID from the social provider
        
    Returns:
        User ID as string or None if creation failed
    """
    db = get_database()
    if db is None:
        return None
    
    user_doc = {
        "name": name,
        "email": email.lower(),
        "password_hash": None,  # No password for social logins
        "social_provider": provider,
        "social_provider_id": provider_id,
        "created_at": datetime.utcnow(),
        "last_login": datetime.utcnow(),
        "is_verified": True,  # Social accounts are pre-verified
        "reset_code": None,
        "reset_code_expires": None
    }
    
    try:
        result = await db[settings.COLLECTION_NAME].insert_one(user_doc)
        return str(result.inserted_id)
    except Exception as e:
        print(f"[ERROR] Error creating social user: {e}")
        return None


async def update_last_login(email: str) -> bool:
    """
    Update user's last login timestamp
    
    Args:
        email: User's email address
        
    Returns:
        True if successful, False otherwise
    """
    db = get_database()
    if db is None:
        return False
    
    try:
        await db[settings.COLLECTION_NAME].update_one(
            {"email": email.lower()},
            {"$set": {"last_login": datetime.utcnow()}}
        )
        return True
    except Exception as e:
        print(f"[ERROR] Error updating last login: {e}")
        return False


async def set_reset_code(email: str, code: str, expires_in_minutes: int = 15) -> bool:
    """
    Set password reset code for user
    
    Args:
        email: User's email address
        code: 6-digit reset code
        expires_in_minutes: Code expiration time in minutes (default: 15)
        
    Returns:
        True if successful, False otherwise
    """
    db = get_database()
    if db is None:
        return False
    
    expires_at = datetime.utcnow() + timedelta(minutes=expires_in_minutes)
    
    try:
        result = await db[settings.COLLECTION_NAME].update_one(
            {"email": email.lower()},
            {
                "$set": {
                    "reset_code": code,
                    "reset_code_expires": expires_at
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"[ERROR] Error setting reset code: {e}")
        return False


async def verify_reset_code(email: str, code: str) -> bool:
    """
    Verify password reset code
    
    Args:
        email: User's email address
        code: 6-digit reset code
        
    Returns:
        True if code is valid and not expired, False otherwise
    """
    db = get_database()
    if db is None:
        return False
    
    user = await get_user_by_email(email)
    if not user:
        return False
    
    # Check if code matches
    if user.get("reset_code") != code:
        return False
    
    # Check if code is expired
    expires_at = user.get("reset_code_expires")
    if not expires_at or datetime.utcnow() > expires_at:
        return False
    
    return True


async def update_password(email: str, new_password: str) -> bool:
    """
    Update user's password
    
    Args:
        email: User's email address
        new_password: New plain text password (will be hashed)
        
    Returns:
        True if successful, False otherwise
    """
    db = get_database()
    if db is None:
        return False
    
    password_hash = hash_password(new_password)
    
    try:
        result = await db[settings.COLLECTION_NAME].update_one(
            {"email": email.lower()},
            {
                "$set": {
                    "password_hash": password_hash,
                    "reset_code": None,
                    "reset_code_expires": None
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"[ERROR] Error updating password: {e}")
        return False


async def clear_reset_code(email: str) -> bool:
    """
    Clear password reset code
    
    Args:
        email: User's email address
        
    Returns:
        True if successful, False otherwise
    """
    db = get_database()
    if db is None:
        return False
    
    try:
        await db[settings.COLLECTION_NAME].update_one(
            {"email": email.lower()},
            {
                "$set": {
                    "reset_code": None,
                    "reset_code_expires": None
                }
            }
        )
        return True
    except Exception as e:
        print(f"[ERROR] Error clearing reset code: {e}")
        return False
