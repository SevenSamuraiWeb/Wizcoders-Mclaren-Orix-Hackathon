"""
Authentication Endpoint Tests

Tests for user login, token refresh, and authentication.
"""

import pytest
from fastapi import status
from src.models import TokenResponse


@pytest.mark.unit
def test_login_success(client):
    """Test successful user login."""
    payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    response = client.post("/api/v1/auth/login", json=payload)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] > 0


@pytest.mark.unit
def test_login_invalid_email(client):
    """Test login with invalid email format."""
    payload = {
        "email": "invalid-email",
        "password": "password123"
    }
    
    response = client.post("/api/v1/auth/login", json=payload)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.unit
def test_login_missing_password(client):
    """Test login with missing password."""
    payload = {
        "email": "test@example.com",
        "password": ""
    }
    
    response = client.post("/api/v1/auth/login", json=payload)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.unit
def test_get_current_user(client, headers_with_auth):
    """Test getting current user information."""
    response = client.get("/api/v1/auth/me", headers=headers_with_auth)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert "name" in data
    assert "role" in data
