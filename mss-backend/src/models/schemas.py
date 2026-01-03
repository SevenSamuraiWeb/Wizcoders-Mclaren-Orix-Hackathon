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


class RiskFactor(BaseModel):
    """Risk factor identified in document."""
    factor: str = Field(description="Name of the risk factor")
    severity: str = Field(description="Severity level: LOW, MEDIUM, HIGH, CRITICAL")
    description: Optional[str] = Field(description="Detailed description of the risk")
    recommendation: Optional[str] = Field(description="Recommended action")


class DocumentAnalysisResponse(BaseModel):
    """Response model for document analysis."""

    status: str = Field(description="Processing status")
    document_id: str = Field(description="Processed document ID")
    analysis: Dict[str, Any] = Field(description="Analysis results")
    extracted_metrics: Optional[Dict[str, Any]] = Field(description="Extracted metrics")
    risk_factors: Optional[List[RiskFactor]] = Field(default=[], description="Identified risk factors")
    recommendations: Optional[List[str]] = Field(default=[], description="Strategic recommendations")
    processing_time_ms: int = Field(description="Processing time in milliseconds")
    processing_method: Optional[str] = Field(default="RAG_pipeline", description="Processing method used")

    class Config:
        example = {
            "status": "success",
            "document_id": "550e8400-e29b-41d4-a716-446655440000",
            "analysis": {
                "summary": "Financial metrics extracted successfully using RAG pipeline",
                "document_type": "credit_memo",
                "confidence": 0.95,
                "ai_insights": "Comprehensive financial analysis..."
            },
            "extracted_metrics": {
                "total_debt": 1000000,
                "total_equity": 500000,
                "debt_to_equity_ratio": 2.0,
                "current_ratio": 1.8
            },
            "risk_factors": [
                {
                    "factor": "High leverage ratio",
                    "severity": "MEDIUM",
                    "description": "Debt-to-equity ratio indicates elevated financial risk",
                    "recommendation": "Consider debt reduction strategies"
                }
            ],
            "recommendations": [
                "Reduce debt levels and improve equity position",
                "Improve liquidity by increasing current assets"
            ],
            "processing_time_ms": 1500,
            "processing_method": "RAG_pipeline"
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
# RAG Pipeline Models
# ============================================================================

class SemanticSearchQuery(BaseModel):
    """Request model for semantic search."""
    query: str = Field(description="Search query text", min_length=1)
    top_k: int = Field(default=3, ge=1, le=10, description="Number of results to return")
    
    class Config:
        example = {
            "query": "financial performance and growth metrics",
            "top_k": 5
        }


class SemanticSearchResult(BaseModel):
    """Result from semantic search."""
    document_id: str = Field(description="Document ID")
    chunk_index: int = Field(description="Index of the text chunk")
    text_preview: str = Field(description="Preview of the matched text")
    similarity_score: float = Field(ge=0.0, le=1.0, description="Similarity score (0-1)")
    
    class Config:
        example = {
            "document_id": "550e8400-e29b-41d4-a716-446655440000",
            "chunk_index": 2,
            "text_preview": "Total Revenue: $15,000,000 Net Income: $2,500,000 The company has demonstrated...",
            "similarity_score": 0.92
        }


class MetricsExtraction(BaseModel):
    """Extracted financial metrics from document."""
    total_revenue: Optional[float] = Field(None, description="Total revenue")
    net_income: Optional[float] = Field(None, description="Net income/profit")
    total_debt: Optional[float] = Field(None, description="Total debt")
    total_equity: Optional[float] = Field(None, description="Total equity/shareholders' equity")
    current_assets: Optional[float] = Field(None, description="Current assets")
    current_liabilities: Optional[float] = Field(None, description="Current liabilities")
    cash_flow: Optional[float] = Field(None, description="Operating cash flow")
    ebitda: Optional[float] = Field(None, description="EBITDA (Earnings Before Interest, Taxes, Depreciation, Amortization)")
    debt_to_equity_ratio: Optional[float] = Field(None, description="Debt to equity ratio")
    current_ratio: Optional[float] = Field(None, description="Current ratio")
    interest_coverage_ratio: Optional[float] = Field(None, description="Interest coverage ratio")
    
    class Config:
        example = {
            "total_revenue": 15000000.0,
            "net_income": 2500000.0,
            "total_debt": 8000000.0,
            "total_equity": 4500000.0,
            "current_assets": 6000000.0,
            "current_liabilities": 3000000.0,
            "cash_flow": 1800000.0,
            "ebitda": 4200000.0,
            "debt_to_equity_ratio": 1.78,
            "current_ratio": 2.0,
            "interest_coverage_ratio": 3.5
        }


class DocumentMetricsResponse(BaseModel):
    """Response containing document metrics and analysis."""
    document_id: str = Field(description="Document ID")
    metrics: MetricsExtraction = Field(description="Extracted financial metrics")
    risk_factors: List[RiskFactor] = Field(default=[], description="Identified risk factors")
    recommendations: List[str] = Field(default=[], description="Recommendations based on metrics")
    
    class Config:
        example = {
            "document_id": "550e8400-e29b-41d4-a716-446655440000",
            "metrics": {
                "total_revenue": 15000000.0,
                "net_income": 2500000.0,
                "debt_to_equity_ratio": 1.78
            },
            "risk_factors": [],
            "recommendations": []
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
