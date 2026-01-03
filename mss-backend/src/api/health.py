"""
Health Check Routes

Provides endpoints for health checks and API status monitoring.
"""

from fastapi import APIRouter, status
from src.models import HealthCheckResponse
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/status",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check API health and status"
)
async def health_check():
    """
    Health check endpoint.
    
    Returns basic API health information and version.
    
    Returns:
        HealthCheckResponse: Health status with timestamp and version
    """
    return HealthCheckResponse(
        status="healthy",
        version=settings.APP_VERSION
    )


@router.get(
    "/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness Probe",
    description="Kubernetes liveness probe endpoint"
)
async def liveness_probe():
    """
    Liveness probe for container orchestration.
    
    Returns:
        dict: Live status indicator
    """
    return {"status": "alive"}


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    summary="Readiness Probe",
    description="Kubernetes readiness probe endpoint"
)
async def readiness_probe():
    """
    Readiness probe for container orchestration.
    
    Returns:
        dict: Ready status indicator
    """
    return {"status": "ready"}
