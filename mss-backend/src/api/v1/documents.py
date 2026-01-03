"""
Document Analysis Routes

Routes for handling document uploads and analysis.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends, BackgroundTasks
from src.models import DocumentAnalysisRequest, DocumentAnalysisResponse
from src.services.document_service import DocumentService
from src.core.security import SecurityManager
from src.core.config import settings
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


# Service instance
document_service = DocumentService()


@router.post(
    "/documents/upload",
    response_model=DocumentAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload and Analyze Document",
    description="Upload a PDF document for AI-powered financial analysis"
)
async def upload_document(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None
):
    """
    Upload and analyze a financial document.
    
    Validates file, processes PDF, and performs AI analysis.
    
    Args:
        file: PDF file to upload
        background_tasks: Background task queue for async processing
        
    Returns:
        DocumentAnalysisResponse: Analysis results
        
    Raises:
        HTTPException 400: Invalid file format
        HTTPException 413: File too large
        HTTPException 422: File reading error
        HTTPException 500: Processing error
    """
    start_time = datetime.utcnow()
    
    try:
        # Validate file
        content = await file.read()
        file_size = len(content)
        
        SecurityManager.validate_file_upload(file.filename, file_size)
        
        # Generate unique document ID
        document_id = str(uuid.uuid4())
        sanitized_filename = SecurityManager.sanitize_filename(file.filename)
        
        # Process document
        analysis_result = await document_service.process_document(
            document_id=document_id,
            filename=sanitized_filename,
            content=content
        )
        
        # Calculate processing time
        processing_time_ms = int(
            (datetime.utcnow() - start_time).total_seconds() * 1000
        )
        
        return DocumentAnalysisResponse(
            status="success",
            document_id=document_id,
            analysis=analysis_result.get("analysis", {}),
            extracted_metrics=analysis_result.get("metrics", {}),
            processing_time_ms=processing_time_ms
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing document: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing document"
        )
    finally:
        await file.close()


@router.get(
    "/documents/{document_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Get Document Analysis",
    description="Retrieve analysis results for a processed document"
)
async def get_document_analysis(document_id: str):
    """
    Get analysis results for a document.
    
    Args:
        document_id: ID of the document
        
    Returns:
        dict: Document analysis results
        
    Raises:
        HTTPException 404: Document not found
    """
    try:
        analysis = await document_service.get_document_analysis(document_id)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        return analysis
    except Exception as e:
        logger.error(f"Error retrieving document analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving document"
        )
