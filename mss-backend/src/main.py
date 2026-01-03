"""
MSS Financial Analysis Platform - Main Application Entry Point

This module initializes and configures the FastAPI application with
all necessary middleware, routes, and error handlers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging

from src.core.config import settings
from src.core.logging_config import setup_logging
from src.api.v1.routes import router as api_router
from src.api.health import router as health_router

# Setup logging
logger = setup_logging(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise-grade AI-powered financial document analysis",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    redoc_url="/api/redoc",
)

# ============================================================================
# Middleware Configuration
# ============================================================================

# Security middleware: TrustedHost
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# CORS middleware - Configurable by environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    # Don't expose internal details in production
    if settings.DEBUG:
        detail = str(exc)
    else:
        detail = "An unexpected error occurred. Please try again later."
    
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": detail,
            "code": "INTERNAL_SERVER_ERROR"
        }
    )


# ============================================================================
# Routes Registration
# ============================================================================

# Health check routes
app.include_router(health_router, prefix="/health", tags=["health"])

# API v1 routes
app.include_router(api_router, prefix="/api/v1", tags=["api"])


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("Application shutting down")
    logger.info("Application shutdown complete")


# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
        "health": "/health/status"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS if not settings.DEBUG else 1,
        log_level=settings.LOG_LEVEL.lower(),
    )
