import os
import secrets
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URI: str = os.getenv(
        "MONGODB_URI",
        "mongodb+srv://stam:Pass1122@cluster0.ru8ccqx.mongodb.net/HomeAssignment?authSource=admin&retryWrites=true&w=majority"
    )
    DATABASE_NAME: str = "HomeAssignment"
    COLLECTION_NAME: str = "users"
    
    # JWT Configuration
    JWT_SECRET: str = os.getenv("JWT_SECRET", secrets.token_urlsafe(32))
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24
    
    # OAuth Credentials - Google
    GOOGLE_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/api/auth/google/callback")
    
    # OAuth Credentials - Facebook
    FACEBOOK_APP_ID: Optional[str] = os.getenv("FACEBOOK_APP_ID")
    FACEBOOK_APP_SECRET: Optional[str] = os.getenv("FACEBOOK_APP_SECRET")
    FACEBOOK_REDIRECT_URI: str = os.getenv("FACEBOOK_REDIRECT_URI", "http://localhost:8000/api/auth/facebook/callback")
    
    # Email Service
    EMAIL_SERVICE: str = os.getenv("EMAIL_SERVICE", "console")  # "azure", "sendgrid", or "console"
    AZURE_COMMUNICATION_CONNECTION_STRING: Optional[str] = os.getenv("AZURE_COMMUNICATION_CONNECTION_STRING")
    SENDGRID_API_KEY: Optional[str] = os.getenv("SENDGRID_API_KEY")
    FROM_EMAIL: str = os.getenv("FROM_EMAIL", "noreply@example.com")
    
    # Frontend URLs
    FRONTEND_URL_WEB: str = os.getenv("FRONTEND_URL_WEB", "http://localhost:5173")
    FRONTEND_URL_MOBILE: str = os.getenv("FRONTEND_URL_MOBILE", "exp://localhost:19000")
    
    # Server Configuration
    NODE_WELCOME_SERVICE_URL: str = os.getenv("NODE_WELCOME_SERVICE_URL", "http://localhost:3000/welcome-message")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
