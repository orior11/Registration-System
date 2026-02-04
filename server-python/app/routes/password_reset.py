from fastapi import APIRouter, HTTPException, status
from datetime import datetime, timedelta
import random
from app.models import PasswordResetRequest, PasswordResetVerify, PasswordResetComplete, PasswordResetResponse
from app.services.user_service import get_user_by_email, set_reset_code, update_password
from app.services.email_service import send_reset_code

router = APIRouter(prefix="/api/password-reset", tags=["Password Reset"])


def generate_reset_code() -> str:
    """Generate a 6-digit reset code"""
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


@router.post("/request", response_model=PasswordResetResponse, summary="Request Password Reset")
async def request_password_reset(request: PasswordResetRequest):
    """
    Request a password reset code
    
    Sends a 6-digit code to the user's email that expires in 15 minutes
    """
    # Check if user exists
    user = await get_user_by_email(request.email)
    
    if not user:
        # Don't reveal if user exists or not for security
        return {
            "success": True,
            "message": "If the email exists, a reset code has been sent"
        }
    
    # Check if user registered with social provider
    if user.get("social_provider"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please login with your social account"
        )
    
    # Generate reset code
    reset_code = generate_reset_code()
    
    # Save reset code to database (expires in 15 minutes)
    await set_reset_code(request.email, reset_code, expires_in_minutes=15)
    
    # Send email with reset code
    email_sent = await send_reset_code(request.email, reset_code)
    
    if not email_sent:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send reset code"
        )
    
    return {
        "success": True,
        "message": "Reset code sent to your email"
    }


@router.post("/verify", response_model=PasswordResetResponse, summary="Verify Reset Code")
async def verify_reset_code(request: PasswordResetVerify):
    """
    Verify the reset code
    
    Checks if the code is valid and not expired
    """
    # Get user
    user = await get_user_by_email(request.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if reset code exists
    if not user.get("reset_code"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No reset code found. Please request a new one"
        )
    
    # Check if code matches
    if user["reset_code"] != request.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset code"
        )
    
    # Check if code is expired
    if user.get("reset_code_expires") and user["reset_code_expires"] < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset code has expired. Please request a new one"
        )
    
    return {
        "success": True,
        "message": "Reset code verified successfully"
    }


@router.post("/complete", response_model=PasswordResetResponse, summary="Complete Password Reset")
async def complete_password_reset(request: PasswordResetComplete):
    """
    Complete the password reset process
    
    Updates the user's password after verifying the reset code
    """
    # Get user
    user = await get_user_by_email(request.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if reset code exists
    if not user.get("reset_code"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No reset code found. Please request a new one"
        )
    
    # Check if code matches
    if user["reset_code"] != request.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset code"
        )
    
    # Check if code is expired
    if user.get("reset_code_expires") and user["reset_code_expires"] < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset code has expired. Please request a new one"
        )
    
    # Update password
    await update_password(request.email, request.new_password)
    
    return {
        "success": True,
        "message": "Password reset successfully"
    }
