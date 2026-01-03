"""
Authentication Routes

Routes for user authentication and token management.
"""

from fastapi import APIRouter, HTTPException, status, Depends
from src.models import LoginRequest, TokenResponse, UserResponse
from src.core.security import SecurityManager
from src.core.config import settings
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/auth/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="Authenticate user and receive JWT token"
)
async def login(request: LoginRequest):
    """
    User login endpoint.
    
    Validates credentials and returns JWT access token.
    
    Args:
        request: Login credentials (email, password)
        
    Returns:
        TokenResponse: JWT access token and expiration info
        
    Raises:
        HTTPException 401: Invalid credentials
    """
    try:
        # TODO: Validate against actual user database
        # For demo: accept any email with valid format
        if not request.email or not request.password:
            raise ValueError("Invalid credentials")
        
        # Create access token
        access_token = SecurityManager.create_access_token(
            data={"sub": request.email, "type": "access"},
            expires_delta=timedelta(hours=settings.JWT_EXPIRATION_HOURS)
        )
        
        logger.info(f"User logged in: {request.email}")
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRATION_HOURS * 3600
        )
        
    except Exception as e:
        logger.warning(f"Login failed for {request.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


@router.get(
    "/auth/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Current User",
    description="Get information about the authenticated user"
)
async def get_current_user():
    """
    Get current authenticated user information.
    
    Returns:
        UserResponse: Current user details
        
    Raises:
        HTTPException 401: Not authenticated
    """
    # TODO: Implement actual user retrieval from database
    # For demo, return placeholder user
    return UserResponse(
        id="demo_user",
        email="demo@example.com",
        name="Demo User",
        role="analyst",
        created_at="2025-01-01T00:00:00"
    )


@router.post(
    "/auth/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh Token",
    description="Get a new access token using refresh token"
)
async def refresh_token(refresh_token: str):
    """
    Refresh access token.
    
    Args:
        refresh_token: Valid refresh token
        
    Returns:
        TokenResponse: New access token
        
    Raises:
        HTTPException 401: Invalid refresh token
    """
    try:
        # Verify refresh token
        payload = SecurityManager.verify_token(refresh_token)
        
        # Create new access token
        access_token = SecurityManager.create_access_token(
            data={"sub": payload.get("sub"), "type": "access"}
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.JWT_EXPIRATION_HOURS * 3600
        )
        
    except Exception as e:
        logger.warning(f"Token refresh failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
