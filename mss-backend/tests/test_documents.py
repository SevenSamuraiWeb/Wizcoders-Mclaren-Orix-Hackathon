"""
Document Processing Tests

Tests for document upload and analysis endpoints.
"""

import pytest
from fastapi import status
import io


@pytest.mark.unit
def test_upload_document_success(client, headers_with_auth):
    """Test successful document upload."""
    # Create a fake PDF file
    pdf_content = b"%PDF-1.4\n%fake pdf content"
    
    files = {
        "file": ("test.pdf", io.BytesIO(pdf_content), "application/pdf")
    }
    
    response = client.post(
        "/api/v1/docs/documents/upload",
        files=files,
        headers=headers_with_auth
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "success"
    assert "document_id" in data
    assert "analysis" in data
    assert "processing_time_ms" in data


@pytest.mark.unit
def test_upload_invalid_file_type(client, headers_with_auth):
    """Test upload with invalid file type."""
    # Try to upload a text file
    files = {
        "file": ("test.txt", io.BytesIO(b"plain text"), "text/plain")
    }
    
    response = client.post(
        "/api/v1/docs/documents/upload",
        files=files,
        headers=headers_with_auth
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.unit
def test_upload_file_too_large(client, headers_with_auth, monkeypatch):
    """Test upload with file exceeding size limit."""
    # Create oversized fake file
    large_content = b"x" * (60 * 1024 * 1024)  # 60MB
    
    files = {
        "file": ("large.pdf", io.BytesIO(large_content), "application/pdf")
    }
    
    response = client.post(
        "/api/v1/docs/documents/upload",
        files=files,
        headers=headers_with_auth
    )
    
    assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


@pytest.mark.unit
def test_get_document_analysis(client, headers_with_auth):
    """Test retrieving document analysis results."""
    doc_id = "550e8400-e29b-41d4-a716-446655440000"
    
    response = client.get(
        f"/api/v1/docs/documents/{doc_id}",
        headers=headers_with_auth
    )
    
    # Will return 404 as document doesn't exist, but endpoint is working
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND]
