"""
Health Check Endpoint Tests

Tests for health check and status endpoints.
"""

import pytest
from fastapi import status


@pytest.mark.unit
def test_health_status(client):
    """Test health status endpoint returns healthy."""
    response = client.get("/health/status")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


@pytest.mark.unit
def test_liveness_probe(client):
    """Test liveness probe endpoint."""
    response = client.get("/health/live")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "alive"


@pytest.mark.unit
def test_readiness_probe(client):
    """Test readiness probe endpoint."""
    response = client.get("/health/ready")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ready"


@pytest.mark.unit
def test_root_endpoint(client):
    """Test root endpoint returns API info."""
    response = client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs" in data
