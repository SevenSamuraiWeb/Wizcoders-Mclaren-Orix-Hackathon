"""
API v1 Routes Router

Aggregates all v1 API routes into a single router.
"""

from fastapi import APIRouter
from src.api.v1 import documents, auth

# Create main router
router = APIRouter()

# Include sub-routers
router.include_router(auth.router, prefix="/auth", tags=["authentication"])
router.include_router(documents.router, prefix="/documents", tags=["documents"])

__all__ = ["router"]
