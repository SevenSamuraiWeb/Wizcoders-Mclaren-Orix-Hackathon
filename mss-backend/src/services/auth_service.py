"""
Authentication Service

Handles user authentication, token generation, and credential validation.
This service implements industry-standard security practices.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import jwt
from pydantic import EmailStr

from src.core.config import settings
from src.core.exceptions import (
    AuthenticationError,
    InvalidTokenError,
    InvalidCredentialsError,
)
from src.models.schemas import TokenResponse, UserResponse

logger = logging.getLogger(__name__)
security = HTTPBearer()


class AuthService:
    """
    Service for authentication and authorization operations.

    This service handles:
    - User credential validation
    - JWT token generation and validation
    - User context extraction from tokens
    """

    @staticmethod
    def create_access_token(
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token.

        Args:
            data: Claims to include in the token
            expires_delta: Token expiration time delta

        Returns:
            str: Encoded JWT token

        Raises:
            AuthenticationError: If token creation fails
        """
        try:
            to_encode = data.copy()

            # Set expiration
            if expires_delta:
                expire = datetime.now(timezone.utc) + expires_delta
            else:
                expire = datetime.now(timezone.utc) + timedelta(
                    hours=settings.JWT_EXPIRATION_HOURS
                )

            to_encode.update({"exp": expire})

            # Encode token
            encoded_jwt = jwt.encode(
                to_encode,
                settings.JWT_SECRET_KEY,
                algorithm=settings.JWT_ALGORITHM
            )

            logger.debug(f"Access token created for user: {data.get('sub')}")
            return encoded_jwt

        except Exception as e:
            logger.error(f"Failed to create access token: {e}")
            raise AuthenticationError("Failed to create access token")

    @staticmethod
    def verify_token(token: str) -> Dict[str, Any]:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token to verify

        Returns:
            dict: Decoded token claims

        Raises:
            InvalidTokenError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("Attempt to use expired token")
            raise InvalidTokenError("Token has expired")

        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token attempt: {e}")
            raise InvalidTokenError("Invalid token")

    @staticmethod
    def validate_credentials(email: EmailStr, password: str) -> bool:
        """
        Validate user credentials.

        NOTE: This is a demo implementation. In production, validate
        against a real user database with proper password hashing.

        Args:
            email: User email
            password: User password

        Returns:
            bool: True if credentials are valid

        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        # Validation checks
        if not email or not password:
            raise InvalidCredentialsError()

        if len(password) < 6:
            raise InvalidCredentialsError()

        # Demo: Accept any valid email format
        # TODO: Replace with actual database lookup and password hashing
        logger.info(f"Credential validation passed for: {email}")
        return True

    @staticmethod
    def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> str:
        """
        Extract and validate current user from request.

        This dependency can be used on protected endpoints to ensure
        the request includes a valid authentication token.

        Args:
            credentials: HTTP Bearer token from request

        Returns:
            str: User email (subject claim)

        Raises:
            HTTPException: If authentication fails
        """
        try:
            token = credentials.credentials
            payload = AuthService.verify_token(token)
            email = payload.get("sub")

            if email is None:
                raise InvalidTokenError("Invalid token claims")

            return email

        except (InvalidTokenError, AuthenticationError) as e:
            logger.warning(f"Authentication failed: {e.message}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    def get_user_info(email: str) -> UserResponse:
        """
        Get user information.

        NOTE: This is a demo implementation that returns mock data.
        In production, fetch from actual user database.

        Args:
            email: User email

        Returns:
            UserResponse: User information
        """
        return UserResponse(
            id="user_123",
            email=email,
            name=email.split("@")[0].title(),
            created_at=datetime.now(timezone.utc),
        )


__all__ = ["AuthService", "security"]
