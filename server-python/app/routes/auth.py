"""
Authentication Routes - Login, OAuth (Google, Facebook)
"""
from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.responses import RedirectResponse
from datetime import datetime
from app.models import LoginRequest, LoginResponse, OAuthCallbackResponse
from app.auth.password import verify_password
from app.auth.jwt_handler import create_access_token
from app.auth.oauth import oauth
from app.services.user_service import (
    get_user_by_email, 
    update_last_login,
    create_social_user
)
from app.config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/login", response_model=LoginResponse)
@limiter.limit("10/minute")
async def login(request: Request, credentials: LoginRequest):
    """
    Login with email and password
    
    - Validates email and password
    - Returns JWT access token on success
    - Updates last login timestamp
    """
    # Find user by email
    user = await get_user_by_email(credentials.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user has a password (not a social login account)
    if not user.get("password_hash"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This account uses social login. Please use Google or Facebook to sign in."
        )
    
    # Verify password
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Update last login
    await update_last_login(credentials.email)
    
    # Generate JWT token
    user_id = str(user["_id"])
    access_token = create_access_token(user_id, credentials.email)
    
    return LoginResponse(
        success=True,
        message="Login successful",
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user_id,
            "name": user["name"],
            "email": user["email"],
            "social_provider": user.get("social_provider")
        }
    )


# ============================================
# GOOGLE OAUTH
# ============================================

@router.get("/google/login")
async def google_login(request: Request):
    """
    Initiate Google OAuth login flow
    
    Redirects user to Google's authentication page
    """
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth is not configured"
        )
    
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(request: Request):
    """
    Handle Google OAuth callback
    
    - Receives authorization code from Google
    - Exchanges it for user info
    - Creates account if new user
    - Returns JWT token
    """
    if not settings.GOOGLE_CLIENT_ID or not settings.GOOGLE_CLIENT_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google OAuth is not configured"
        )
    
    try:
        # Get access token from Google
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to get user info from Google"
            )
        
        email = user_info.get('email')
        name = user_info.get('name', email.split('@')[0])
        google_id = user_info.get('sub')
        
        if not email or not google_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incomplete user information from Google"
            )
        
        # Check if user already exists
        user = await get_user_by_email(email)
        
        if not user:
            # Create new user
            user_id = await create_social_user(name, email, "google", google_id)
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user account"
                )
            user = await get_user_by_email(email)
        else:
            # Update last login
            await update_last_login(email)
        
        # Generate JWT token
        user_id = str(user["_id"])
        access_token = create_access_token(user_id, email)
        
        # Redirect to frontend with token
        frontend_url = f"{settings.FRONTEND_URL_WEB}/auth/callback?token={access_token}"
        return RedirectResponse(url=frontend_url)
        
    except Exception as e:
        print(f"[ERROR] Google OAuth error: {e}")
        # Redirect to frontend with error
        error_url = f"{settings.FRONTEND_URL_WEB}/auth/callback?error=oauth_failed"
        return RedirectResponse(url=error_url)


# ============================================
# FACEBOOK OAUTH
# ============================================

@router.get("/facebook/login")
async def facebook_login(request: Request):
    """
    Initiate Facebook OAuth login flow
    
    Redirects user to Facebook's authentication page
    """
    if not settings.FACEBOOK_APP_ID or not settings.FACEBOOK_APP_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Facebook OAuth is not configured"
        )
    
    redirect_uri = settings.FACEBOOK_REDIRECT_URI
    return await oauth.facebook.authorize_redirect(request, redirect_uri)


@router.get("/facebook/callback")
async def facebook_callback(request: Request):
    """
    Handle Facebook OAuth callback
    
    - Receives authorization code from Facebook
    - Exchanges it for user info
    - Creates account if new user
    - Returns JWT token
    """
    if not settings.FACEBOOK_APP_ID or not settings.FACEBOOK_APP_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Facebook OAuth is not configured"
        )
    
    try:
        # Get access token from Facebook
        token = await oauth.facebook.authorize_access_token(request)
        
        # Get user info from Facebook
        resp = await oauth.facebook.get('me?fields=id,name,email', token=token)
        user_info = resp.json()
        
        email = user_info.get('email')
        name = user_info.get('name', 'Facebook User')
        facebook_id = user_info.get('id')
        
        if not email or not facebook_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incomplete user information from Facebook"
            )
        
        # Check if user already exists
        user = await get_user_by_email(email)
        
        if not user:
            # Create new user
            user_id = await create_social_user(name, email, "facebook", facebook_id)
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user account"
                )
            user = await get_user_by_email(email)
        else:
            # Update last login
            await update_last_login(email)
        
        # Generate JWT token
        user_id = str(user["_id"])
        access_token = create_access_token(user_id, email)
        
        # Redirect to frontend with token
        frontend_url = f"{settings.FRONTEND_URL_WEB}/auth/callback?token={access_token}"
        return RedirectResponse(url=frontend_url)
        
    except Exception as e:
        print(f"[ERROR] Facebook OAuth error: {e}")
        # Redirect to frontend with error
        error_url = f"{settings.FRONTEND_URL_WEB}/auth/callback?error=oauth_failed"
        return RedirectResponse(url=error_url)


# ============================================
# USER PROFILE (Protected Route Example)
# ============================================

@router.get("/me")
async def get_current_user_profile(request: Request):
    """
    Get current authenticated user's profile
    
    Requires valid JWT token in Authorization header
    """
    from app.auth.jwt_handler import get_current_user
    
    try:
        user = await get_current_user(request)
        
        return {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "social_provider": user.get("social_provider"),
            "created_at": user["created_at"].isoformat() if user.get("created_at") else None,
            "last_login": user["last_login"].isoformat() if user.get("last_login") else None,
            "is_verified": user.get("is_verified", False)
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Error getting user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )
