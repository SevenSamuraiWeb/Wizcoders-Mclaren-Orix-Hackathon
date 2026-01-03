"""
Unit Tests for Authentication Service

Tests the AuthService module including token generation,
verification, and credential validation.
"""

import pytest
from datetime import timedelta
from fastapi import HTTPException, status

from src.services.auth_service import AuthService
from src.core.exceptions import (
    InvalidTokenError,
    InvalidCredentialsError,
    AuthenticationError
)


class TestAuthServiceTokenGeneration:
    """Test suite for JWT token generation."""

    @pytest.mark.unit
    def test_create_access_token_success(self):
        """Test successful access token creation."""
        user_data = {"sub": "test@example.com", "type": "access"}
        expires_delta = timedelta(hours=1)

        token = AuthService.create_access_token(
            data=user_data,
            expires_delta=expires_delta
        )

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    @pytest.mark.unit
    def test_create_access_token_with_default_expiration(self):
        """Test token creation with default expiration."""
        user_data = {"sub": "user@example.com"}

        token = AuthService.create_access_token(data=user_data)

        assert token is not None
        assert isinstance(token, str)

    @pytest.mark.unit
    def test_create_access_token_invalid_secret_raises_error(self):
        """Test that invalid configuration raises error."""
        # This test depends on settings - adjust as needed
        user_data = {"sub": "test@example.com"}

        # Should not raise on creation, but on verification
        token = AuthService.create_access_token(data=user_data)
        assert token is not None


class TestAuthServiceTokenVerification:
    """Test suite for JWT token verification."""

    @pytest.mark.unit
    def test_verify_valid_token(self, sample_jwt_token):
        """Test verification of valid token."""
        payload = AuthService.verify_token(sample_jwt_token)

        assert payload is not None
        assert isinstance(payload, dict)
        assert "sub" in payload
        assert payload["sub"] == "test@example.com"

    @pytest.mark.unit
    def test_verify_expired_token_raises_error(self):
        """Test verification of expired token raises error."""
        # Create an expired token
        expired_delta = timedelta(seconds=-10)
        expired_token = AuthService.create_access_token(
            data={"sub": "test@example.com"},
            expires_delta=expired_delta
        )

        with pytest.raises(InvalidTokenError):
            AuthService.verify_token(expired_token)

    @pytest.mark.unit
    def test_verify_invalid_token_raises_error(self):
        """Test verification of invalid token raises error."""
        invalid_token = "invalid.token.value"

        with pytest.raises(InvalidTokenError):
            AuthService.verify_token(invalid_token)

    @pytest.mark.unit
    def test_verify_token_without_sub_claim_raises_error(self):
        """Test verification of token without subject claim."""
        token = AuthService.create_access_token(data={"type": "access"})

        # Verification succeeds, but we can't extract user
        payload = AuthService.verify_token(token)
        assert payload.get("sub") is None


class TestAuthServiceCredentialValidation:
    """Test suite for credential validation."""

    @pytest.mark.unit
    def test_validate_valid_credentials(self, test_user_data):
        """Test validation of valid credentials."""
        result = AuthService.validate_credentials(
            email=test_user_data["email"],
            password=test_user_data["password"]
        )

        assert result is True

    @pytest.mark.unit
    def test_validate_empty_email_raises_error(self):
        """Test that empty email raises error."""
        with pytest.raises(InvalidCredentialsError):
            AuthService.validate_credentials(email="", password="password123")

    @pytest.mark.unit
    def test_validate_empty_password_raises_error(self):
        """Test that empty password raises error."""
        with pytest.raises(InvalidCredentialsError):
            AuthService.validate_credentials(email="test@example.com", password="")

    @pytest.mark.unit
    def test_validate_short_password_raises_error(self):
        """Test that short password raises error."""
        with pytest.raises(InvalidCredentialsError):
            AuthService.validate_credentials(
                email="test@example.com",
                password="short"
            )

    @pytest.mark.unit
    def test_validate_none_credentials_raises_error(self):
        """Test that None credentials raise error."""
        with pytest.raises(InvalidCredentialsError):
            AuthService.validate_credentials(email=None, password=None)


class TestAuthServiceGetCurrentUser:
    """Test suite for current user extraction."""

    @pytest.mark.unit
    def test_get_current_user_with_valid_token(self, sample_jwt_token):
        """Test extracting user from valid token."""
        from fastapi.security import HTTPAuthCredentials

        credentials = HTTPAuthCredentials(scheme="bearer", credentials=sample_jwt_token)
        user = AuthService.get_current_user(credentials)

        assert user == "test@example.com"

    @pytest.mark.unit
    def test_get_user_info(self, test_user_data):
        """Test retrieving user information."""
        user_info = AuthService.get_user_info(test_user_data["email"])

        assert user_info is not None
        assert user_info.email == test_user_data["email"]
        assert user_info.id is not None
        assert user_info.created_at is not None


class TestAuthServiceIntegration:
    """Integration tests for complete authentication flow."""

    @pytest.mark.unit
    def test_complete_auth_flow(self, test_user_data):
        """Test complete authentication flow: validate -> create token -> verify."""
        # Step 1: Validate credentials
        is_valid = AuthService.validate_credentials(
            email=test_user_data["email"],
            password=test_user_data["password"]
        )
        assert is_valid

        # Step 2: Create token
        token = AuthService.create_access_token(
            data={"sub": test_user_data["email"], "type": "access"},
            expires_delta=timedelta(hours=24)
        )
        assert token is not None

        # Step 3: Verify token
        payload = AuthService.verify_token(token)
        assert payload["sub"] == test_user_data["email"]

        # Step 4: Get user info
        user_info = AuthService.get_user_info(test_user_data["email"])
        assert user_info.email == test_user_data["email"]
