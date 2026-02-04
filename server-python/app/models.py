"""
Pydantic Models for API Request/Response Validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re


class RegistrationRequest(BaseModel):
    """User registration request model"""
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=100, description="User's password")
    
    @validator('password')
    def validate_password_strength(cls, v):
        """
        Validate password strength:
        - At least 8 characters
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        """
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        
        return v
    
    @validator('name')
    def validate_name(cls, v):
        """Validate name contains only letters, spaces, and basic punctuation"""
        if not re.match(r'^[a-zA-Z\s\'-]+$', v):
            raise ValueError('Name can only contain letters, spaces, hyphens, and apostrophes')
        return v.strip()


class RegistrationResponse(BaseModel):
    """User registration response model"""
    success: bool
    message: str
    welcome_message: Optional[str] = None


class LoginRequest(BaseModel):
    """User login request model"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=1, description="User's password")


class LoginResponse(BaseModel):
    """User login response model"""
    success: bool
    message: str
    access_token: Optional[str] = None
    token_type: str = "bearer"
    user: Optional[dict] = None


class PasswordResetRequest(BaseModel):
    """Password reset request - Step 1: Request reset code"""
    email: EmailStr = Field(..., description="User's email address")


class PasswordResetVerify(BaseModel):
    """Password reset verification - Step 2: Verify reset code"""
    email: EmailStr = Field(..., description="User's email address")
    code: str = Field(..., min_length=6, max_length=6, description="6-digit reset code")
    
    @validator('code')
    def validate_code_format(cls, v):
        """Validate code is exactly 6 digits"""
        if not v.isdigit():
            raise ValueError('Code must contain only digits')
        if len(v) != 6:
            raise ValueError('Code must be exactly 6 digits')
        return v


class PasswordResetComplete(BaseModel):
    """Password reset completion - Step 3: Set new password"""
    email: EmailStr = Field(..., description="User's email address")
    code: str = Field(..., min_length=6, max_length=6, description="6-digit reset code")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    @validator('new_password')
    def validate_password_strength(cls, v):
        """Validate new password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        
        return v


class PasswordResetResponse(BaseModel):
    """Generic password reset response"""
    success: bool
    message: str


class UserResponse(BaseModel):
    """User profile response model"""
    id: str
    name: str
    email: EmailStr
    social_provider: Optional[str] = None
    created_at: str
    last_login: Optional[str] = None
    is_verified: bool


class OAuthCallbackResponse(BaseModel):
    """OAuth callback response model"""
    success: bool
    message: str
    access_token: Optional[str] = None
    token_type: str = "bearer"
    user: Optional[dict] = None
