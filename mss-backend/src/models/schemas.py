"""
Data Models Module

Pydantic models for request/response validation and data consistency.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


# ============================================================================
# File/Document Models
# ============================================================================

class DocumentAnalysisRequest(BaseModel):
    """Request model for document analysis."""
    
    file_id: str = Field(description="Unique file identifier")
    file_name: str = Field(description="Original filename")
    file_size: int = Field(description="File size in bytes")
    file_type: str = Field(description="MIME type")
    
    class Config:
        example = {
            "file_id": "550e8400-e29b-41d4-a716-446655440000",
            "file_name": "credit_memo.pdf",
            "file_size": 1048576,
            "file_type": "application/pdf"
        }


class DocumentAnalysisResponse(BaseModel):
    """Response model for document analysis."""
    
    status: str = Field(description="Processing status")
    document_id: str = Field(description="Processed document ID")
    analysis: Dict[str, Any] = Field(description="Analysis results")
    extracted_metrics: Optional[Dict[str, Any]] = Field(description="Extracted metrics")
    processing_time_ms: int = Field(description="Processing time in milliseconds")
    
    class Config:
        example = {
            "status": "success",
            "document_id": "550e8400-e29b-41d4-a716-446655440000",
            "analysis": {"summary": "..."},
            "extracted_metrics": {"total_debt": 1000000},
            "processing_time_ms": 1500
        }


# ============================================================================
# Authentication Models
# ============================================================================

class LoginRequest(BaseModel):
    """Request model for user login."""
    
    email: str = Field(description="User email")
    password: str = Field(description="User password", min_length=1)
    
    @validator('email')
    def validate_email(cls, v):
        """Basic email validation."""
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()
    
    class Config:
        example = {
            "email": "user@example.com",
            "password": "securepassword"
        }


class TokenResponse(BaseModel):
    """Response model for token."""
    
    access_token: str = Field(description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(description="Expiration time in seconds")
    
    class Config:
        example = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "expires_in": 86400
        }


class UserResponse(BaseModel):
    """Response model for user data."""
    
    id: str = Field(description="User ID")
    email: str = Field(description="User email")
    name: Optional[str] = Field(description="User name")
    role: str = Field(description="User role")
    created_at: datetime = Field(description="Account creation date")
    
    class Config:
        example = {
            "id": "user123",
            "email": "user@example.com",
            "name": "John Doe",
            "role": "analyst",
            "created_at": "2025-01-01T00:00:00"
        }


# ============================================================================
# Error Models
# ============================================================================

class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    status: str = Field(default="error", description="Status")
    message: str = Field(description="Error message")
    code: str = Field(description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        example = {
            "status": "error",
            "message": "File processing failed",
            "code": "PROCESSING_ERROR",
            "details": {"reason": "Invalid PDF format"},
            "timestamp": "2025-01-01T12:00:00"
        }


class ValidationErrorResponse(BaseModel):
    """Validation error response model."""
    
    status: str = Field(default="error")
    message: str = Field(default="Validation error")
    code: str = Field(default="VALIDATION_ERROR")
    errors: List[Dict[str, str]] = Field(description="Field-level errors")
    
    class Config:
        example = {
            "status": "error",
            "message": "Validation error",
            "code": "VALIDATION_ERROR",
            "errors": [
                {"field": "email", "message": "Invalid email format"}
            ]
        }


# ============================================================================
# Generic Models
# ============================================================================

class PaginationParams(BaseModel):
    """Pagination parameters."""
    
    skip: int = Field(default=0, ge=0, description="Records to skip")
    limit: int = Field(default=10, ge=1, le=100, description="Records to return")


class HealthCheckResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(description="Health status")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(description="API version")
    
    class Config:
        example = {
            "status": "healthy",
            "timestamp": "2025-01-01T12:00:00",
            "version": "0.1.0"
        }
