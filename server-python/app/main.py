import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.database import connect_to_mongo, close_mongo_connection, get_database
from app.config import settings
from app.models import RegistrationRequest, RegistrationResponse
from app.auth.password import hash_password
from app.routes import auth, password_reset
from app.services.user_service import get_user_by_email

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()


# Initialize FastAPI app
app = FastAPI(
    title="Authentication API",
    description="Secure authentication system with JWT, OAuth, and password reset",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL_WEB,
        settings.FRONTEND_URL_MOBILE,
        "http://localhost:5173",
        "http://localhost:19000",
        "exp://localhost:19000",
        "*"  # Remove in production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Include routers
app.include_router(auth.router)
app.include_router(password_reset.router)


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint"""
    db = get_database()
    return {
        "status": "ok",
        "database": "connected" if db is not None else "disconnected"
    }


# Registration endpoint (kept from original)
@app.post(
    "/api/register",
    response_model=RegistrationResponse,
    summary="User Registration",
    description="Register a new user with email and password"
)
@limiter.limit("5/minute")
async def register(request: Request, user_data: RegistrationRequest):
    """
    Register a new user
    
    - Validates email format and password strength
    - Checks for existing users
    - Hashes password with bcrypt
    - Stores user in MongoDB
    - Calls Node.js service for welcome message (optional)
    """
    # Check if user already exists
    db = get_database()
    existing = await get_user_by_email(user_data.email)
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password
    password_hash = hash_password(user_data.password)
    
    # Create user document
    from datetime import datetime
    user_doc = {
        "name": user_data.name,
        "email": user_data.email,
        "password_hash": password_hash,
        "social_provider": None,
        "social_provider_id": None,
        "created_at": datetime.utcnow(),
        "last_login": None,
        "is_verified": False,
        "reset_code": None,
        "reset_code_expires": None
    }
    
    # Insert into MongoDB
    await db[settings.COLLECTION_NAME].insert_one(user_doc)
    
    # Try to get welcome message from Node.js service
    welcome_msg = "Welcome to our platform!"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.NODE_WELCOME_SERVICE_URL, timeout=5.0)
            if response.status_code == 200:
                welcome_msg = response.json().get("message", welcome_msg)
    except Exception as e:
        print(f"[WARNING] NodeJS Service not reachable: {e}")
    
    return {
        "success": True,
        "message": "User registered successfully",
        "welcome_message": welcome_msg
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Authentication API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
