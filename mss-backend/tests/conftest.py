"""
Test Configuration and Fixtures

This module provides pytest configuration, fixtures, and utilities
for testing the MSS Financial Analysis Platform backend.
"""

import os
import pytest
from pathlib import Path
from typing import Generator
from datetime import timedelta
from fastapi.testclient import TestClient

# Set environment to testing
os.environ["ENVIRONMENT"] = "testing"
os.environ["DEBUG"] = "true"
os.environ["LOG_LEVEL"] = "DEBUG"

from src.main import app
from src.core.config import settings


# ============================================================================
# FastAPI Test Client
# ============================================================================

@pytest.fixture
def client():
    """FastAPI test client for API testing."""
    return TestClient(app)


# ============================================================================
# Authentication Fixtures
# ============================================================================

@pytest.fixture
def sample_jwt_token() -> str:
    """
    Provide a sample JWT token for testing protected endpoints.

    Returns:
        str: Valid JWT token
    """
    from src.services.auth_service import AuthService

    token = AuthService.create_access_token(
        data={"sub": "test@example.com", "type": "access"},
        expires_delta=timedelta(hours=24)
    )
    return token


@pytest.fixture
def auth_headers(sample_jwt_token) -> dict:
    """
    Provide HTTP headers with authentication token.

    Args:
        sample_jwt_token: Valid JWT token

    Returns:
        dict: Headers with authorization
    """
    return {
        "Authorization": f"Bearer {sample_jwt_token}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def test_user_data() -> dict:
    """
    Provide sample user data for testing authentication.

    Returns:
        dict: Sample user credentials
    """
    return {
        "email": "test@example.com",
        "password": "test_password_123",
        "name": "Test User"
    }


# ============================================================================
# Document Testing Fixtures
# ============================================================================

@pytest.fixture
def sample_document_text() -> str:
    """
    Provide sample financial document text for testing document processing.

    Returns:
        str: Sample financial document text
    """
    return """
    FINANCIAL REPORT - Q4 2024
    
    Total Revenue: $5,000,000
    Net Income: $1,200,000
    Operating Expenses: $2,100,000
    
    Balance Sheet Summary:
    Total Assets: $25,000,000
    Total Liabilities: $8,000,000
    Shareholders' Equity: $17,000,000
    
    Key Metrics:
    - Debt-to-Equity Ratio: 0.47
    - Current Ratio: 2.1
    - Profit Margin: 24%
    """


@pytest.fixture
def sample_pdf_file(tmp_path):
    """
    Provide a temporary PDF file for testing file upload.

    Args:
        tmp_path: Pytest temporary directory fixture

    Returns:
        str: Path to sample PDF file
    """
    pdf_path = tmp_path / "sample.pdf"
    # Create a minimal PDF file
    pdf_content = b"%PDF-1.4\n1 0 obj\n<< >>\nendobj\nxref\ntrailer\n<< /Size 1 >>\nstartxref\n0\n%%EOF"
    pdf_path.write_bytes(pdf_content)
    return str(pdf_path)


# ============================================================================
# Pytest Configuration Hooks
# ============================================================================

def pytest_configure(config):
    """
    Configure pytest with custom markers and settings.

    Args:
        config: Pytest config object
    """
    config.addinivalue_line(
        "markers",
        "unit: Mark test as a unit test"
    )
    config.addinivalue_line(
        "markers",
        "integration: Mark test as an integration test"
    )
    config.addinivalue_line(
        "markers",
        "slow: Mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to add markers based on file location.

    Args:
        config: Pytest config object
        items: List of collected test items
    """
    for item in items:
        # Mark tests appropriately
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        else:
            item.add_marker(pytest.mark.unit)
def test_settings():
    """Test configuration settings."""
    return settings


# ============================================================================
# Pytest Configuration
# ============================================================================

def pytest_configure(config):
    """Pytest configuration hook."""
    # Register custom markers
    config.addinivalue_line("markers", "unit: unit tests")
    config.addinivalue_line("markers", "integration: integration tests")
    config.addinivalue_line("markers", "slow: slow tests")


# ============================================================================
# Test Markers
# ============================================================================

# Usage:
# @pytest.mark.unit
# def test_something(): pass
#
# @pytest.mark.integration
# @pytest.mark.asyncio
# async def test_async_something(): pass
#
# Run only unit tests:
# pytest -m unit
#
# Run except slow tests:
# pytest -m "not slow"
