"""
Document Analysis Routes

Routes for handling document uploads and analysis.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends, BackgroundTasks
from fastapi.responses import FileResponse
from typing import Dict, Any
from src.models import DocumentAnalysisRequest, DocumentAnalysisResponse, SemanticSearchQuery, SemanticSearchResult
from src.services.document_service import DocumentService
from src.services.report_service import ReportService
from src.services.word_export_service import WordExportService
from src.core.security import SecurityManager
from src.core.config import settings
import logging
import uuid
from datetime import datetime
from typing import List, Dict, Any
import tempfile
import os

logger = logging.getLogger(__name__)
router = APIRouter()

# Service instance
document_service = DocumentService()

@router.post(
    "/upload",
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

        # Process document with RAG pipeline
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
            risk_factors=analysis_result.get("risk_factors_objects", []),
            recommendations=analysis_result.get("recommendations", []),
            processing_time_ms=processing_time_ms,
            processing_method=analysis_result.get("processing_method", "RAG_pipeline")
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
    "/{document_id}",
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

@router.post(
    "/search",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="Semantic Document Search",
    description="Perform semantic search across processed documents"
)
async def semantic_search(
    request: SemanticSearchQuery
):
    """
    Perform semantic search on processed documents.

    Args:
        request: Search query and parameters

    Returns:
        List of search results with similarity scores

    Raises:
        HTTPException 400: Invalid query
        HTTPException 500: Search error
    """
    try:
        results = await document_service.semantic_search(request.query, request.top_k)

        return [{
            "document_id": result["document_id"],
            "text_preview": result["text"][:200] + "..." if len(result["text"]) > 200 else result["text"],
            "similarity_score": result["similarity_score"],
            "chunk_index": result["chunk_index"]
        } for result in results]

    except Exception as e:
        logger.error(f"Error performing semantic search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error performing semantic search"
        )

@router.get(
    "/{document_id}/metrics",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get Document Metrics",
    description="Retrieve extracted financial metrics for a document"
)
async def get_document_metrics(document_id: str):
    """
    Get extracted financial metrics for a document.

    Args:
        document_id: ID of the document

    Returns:
        dict: Extracted financial metrics

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

        return {
            "document_id": document_id,
            "metrics": analysis.get("metrics", {}),
            "risk_factors": analysis.get("risk_factors", []),
            "recommendations": analysis.get("recommendations", [])
        }

    except Exception as e:
        logger.error(f"Error retrieving document metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving document metrics"
        )


@router.get(
    "/{document_id}/report",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Generate Financial Report",
    description="Generate a comprehensive financial report for a analyzed document"
)
async def generate_report(document_id: str):
    """
    Generate a comprehensive financial report.

    Args:
        document_id: ID of the analyzed document

    Returns:
        dict: Comprehensive financial report

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

        # Get the filename if available
        filename = "Unknown Document"
        if document_id in document_service.processed_documents:
            filename = document_service.processed_documents[document_id].get("filename", filename)

        report = ReportService.generate_financial_report(
            document_id=document_id,
            analysis_result=analysis,
            document_filename=filename
        )

        return report

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating report"
        )


@router.get(
    "/{document_id}/report/html",
    status_code=status.HTTP_200_OK,
    summary="Get Report as HTML",
    description="Get the report formatted as HTML"
)
async def get_report_html(document_id: str):
    """
    Get the report formatted as HTML.

    Args:
        document_id: ID of the analyzed document

    Returns:
        HTML formatted report

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

        # Get the filename
        filename = "Unknown Document"
        if document_id in document_service.processed_documents:
            filename = document_service.processed_documents[document_id].get("filename", filename)

        # Generate report
        report = ReportService.generate_financial_report(
            document_id=document_id,
            analysis_result=analysis,
            document_filename=filename
        )

        # Convert to HTML
        html_content = ReportService.generate_summary_html(report)

        return {
            "content_type": "text/html",
            "body": html_content
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating HTML report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating HTML report"
        )


@router.get(
    "/{document_id}/report/json",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Get Report as JSON",
    description="Get the report as JSON"
)
async def get_report_json(document_id: str):
    """
    Get the report formatted as JSON.

    Args:
        document_id: ID of the analyzed document

    Returns:
        dict: Report in JSON format

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

        # Get the filename
        filename = "Unknown Document"
        if document_id in document_service.processed_documents:
            filename = document_service.processed_documents[document_id].get("filename", filename)

        # Generate and return report
        report = ReportService.generate_financial_report(
            document_id=document_id,
            analysis_result=analysis,
            document_filename=filename
        )

        return report

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating JSON report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating JSON report"
        )


@router.get(
    "/{document_id}/credit-memo",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Generate Credit Memorandum",
    description="Generate a banker-style credit memorandum with DSCR, confidence tags, and data traceability"
)
async def generate_credit_memo(document_id: str):
    """
    Generate a banker-style credit memorandum.
    
    This is the WINNING hackathon output format with:
    - 5-bullet executive summary (credit-memo style)
    - Key metrics table with DSCR
    - Top 3 risks (data-tied)
    - Page-level traceability
    - Confidence tags (Strong data / Incomplete data)

    Args:
        document_id: ID of the analyzed document

    Returns:
        dict: Credit memorandum in banker format

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

        # Get company name if available
        company_name = "TechCorp Inc."  # Default, would extract from analysis
        if document_id in document_service.processed_documents:
            filename = document_service.processed_documents[document_id].get("filename", "Unknown")
        else:
            filename = "Unknown Document"

        # Generate credit memo
        memo = ReportService.generate_credit_memo(
            document_id=document_id,
            analysis_result=analysis,
            document_filename=filename,
            company_name=company_name
        )

        return memo

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating credit memo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating credit memo"
        )


@router.post(
    "/{document_id}/simplify-text",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    summary="Simplify Financial Text",
    description="Rewrite section in simpler language for non-finance audience"
)
async def simplify_financial_text(document_id: str, text: str):
    """
    Rewrite financial text in simpler language.
    
    Shows human-in-the-loop capability.

    Args:
        document_id: ID of the document
        text: Text section to simplify

    Returns:
        dict: Simplified text version

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

        # Call document service to simplify text
        simplified = await document_service.simplify_text(text)

        return {
            "original_text": text,
            "simplified_text": simplified,
            "document_id": document_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error simplifying text: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error simplifying text"
        )


@router.get(
    "/{document_id}/credit-memo/export/word",
    status_code=status.HTTP_200_OK,
    summary="Export Credit Memo as Word Document",
    description="Export the credit memo as a formatted Word (.docx) file"
)
async def export_credit_memo_word(document_id: str):
    """
    Export credit memo as a Word document.
    
    Returns a downloadable .docx file with formatted credit memo.

    Args:
        document_id: ID of the analyzed document

    Returns:
        FileResponse: Word document file

    Raises:
        HTTPException 404: Document not found
        HTTPException 500: Export error
    """
    try:
        # Get analysis
        analysis = await document_service.get_document_analysis(document_id)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        # Get company name if available
        company_name = "TechCorp Inc."
        filename = "Unknown Document"
        if document_id in document_service.processed_documents:
            filename = document_service.processed_documents[document_id].get("filename", "Unknown")

        # Generate credit memo
        memo = ReportService.generate_credit_memo(
            document_id=document_id,
            analysis_result=analysis,
            document_filename=filename,
            company_name=company_name
        )

        # Export to Word
        word_bytes = WordExportService.create_credit_memo_word(
            memo_data=memo,
            filename=f"credit_memo_{document_id}.docx"
        )

        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
            tmp_file.write(word_bytes)
            tmp_path = tmp_file.name

        # Return as file response
        return FileResponse(
            path=tmp_path,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"credit_memo_{document_id}.docx",
            headers={"Content-Disposition": f'attachment; filename="credit_memo_{document_id}.docx"'}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting credit memo to Word: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error exporting credit memo"
        )


@router.get(
    "/{document_id}/credit-memo/export/markdown",
    status_code=status.HTTP_200_OK,
    summary="Export Credit Memo as Markdown",
    description="Export the credit memo as a formatted Markdown file"
)
async def export_credit_memo_markdown(document_id: str):
    """
    Export credit memo as a Markdown document.
    
    Returns a downloadable .md file with credit memo in Markdown format.

    Args:
        document_id: ID of the analyzed document

    Returns:
        FileResponse: Markdown file

    Raises:
        HTTPException 404: Document not found
        HTTPException 500: Export error
    """
    try:
        # Get analysis
        analysis = await document_service.get_document_analysis(document_id)
        if not analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )

        # Get company name if available
        company_name = "TechCorp Inc."
        filename = "Unknown Document"
        if document_id in document_service.processed_documents:
            filename = document_service.processed_documents[document_id].get("filename", "Unknown")

        # Generate credit memo
        memo = ReportService.generate_credit_memo(
            document_id=document_id,
            analysis_result=analysis,
            document_filename=filename,
            company_name=company_name
        )

        # Convert to Markdown
        markdown_content = _convert_memo_to_markdown(memo)

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".md", encoding='utf-8') as tmp_file:
            tmp_file.write(markdown_content)
            tmp_path = tmp_file.name

        # Return as file response
        return FileResponse(
            path=tmp_path,
            media_type="text/markdown",
            filename=f"credit_memo_{document_id}.md",
            headers={"Content-Disposition": f'attachment; filename="credit_memo_{document_id}.md"'}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error exporting credit memo to Markdown: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error exporting credit memo"
        )


def _convert_memo_to_markdown(memo_data: Dict[str, Any]) -> str:
    """Convert credit memo dictionary to Markdown format"""
    
    md = []
    md.append("# CREDIT MEMORANDUM\n")
    md.append(f"**Document ID:** {memo_data.get('document_id', 'N/A')}\n")
    md.append(f"**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
    
    # Executive Summary
    md.append("## Executive Summary\n")
    bullets = memo_data.get("executive_summary_bullets", [])
    for bullet in bullets:
        if isinstance(bullet, dict):
            text = bullet.get("text", str(bullet))
            confidence = bullet.get("source_confidence", "")
            md.append(f"- **{text}**")
            if confidence:
                md.append(f" *[Source: {confidence}]*")
            md.append("\n")
        else:
            md.append(f"- {str(bullet)}\n")
    md.append("\n")
    
    # Key Metrics
    md.append("## Key Metrics\n\n")
    metrics_table = memo_data.get("metrics_table", {})
    if metrics_table:
        md.append("| Metric | Value |\n")
        md.append("|--------|-------|\n")
        for row in metrics_table.get("data", []):
            metric = row.get("metric", "")
            value = row.get("value", "")
            md.append(f"| {metric} | {value} |\n")
    md.append("\n")
    
    # DSCR Analysis
    if "key_ratios" in memo_data:
        md.append("## Debt Service Coverage Ratio (DSCR) Analysis\n\n")
        key_ratios = memo_data.get("key_ratios", {})
        dscr_value = key_ratios.get("dscr", {})
        if isinstance(dscr_value, dict):
            dscr = dscr_value.get("value", "N/A")
        else:
            dscr = dscr_value
        md.append(f"**DSCR:** {dscr}\n\n")
    
    # Top Risks
    md.append("## Top 3 Risks\n\n")
    risks = memo_data.get("top_3_risks", [])
    for i, risk in enumerate(risks, 1):
        severity = risk.get("severity", "UNKNOWN")
        md.append(f"### {i}. {risk.get('risk_factor', f'Risk {i}')} [{severity}]\n\n")
        
        description = risk.get("description", "")
        if description:
            md.append(f"{description}\n\n")
        
        if "severity_justification" in risk:
            justification = risk.get("severity_justification", "")
            md.append(f"**Justification:** {justification}\n\n")
    
    # Missing Information
    if "missing_information" in memo_data:
        missing = memo_data.get("missing_information", [])
        if missing:
            md.append("## Missing Information\n\n")
            for item in missing:
                md.append(f"- {item}\n")
            md.append("\n")
    
    # Red Flags
    if "red_flags" in memo_data:
        red_flags = memo_data.get("red_flags", [])
        if red_flags:
            md.append("## Red Flags Detected\n\n")
            for flag in red_flags:
                flag_name = flag.get("flag", "Flag")
                severity = flag.get("severity", "")
                md.append(f"### {flag_name} [{severity}]\n\n")
                if flag.get("description"):
                    md.append(f"{flag.get('description')}\n\n")
    
    # Credit Analyst Checklist
    if "credit_analyst_checklist" in memo_data:
        checklist = memo_data.get("credit_analyst_checklist", {})
        if checklist:
            md.append("## Credit Analyst Checklist\n\n")
            
            reviewed = checklist.get("reviewed_documents", {})
            if reviewed:
                md.append("### Documents Reviewed\n\n")
                for doc_name, status in reviewed.items():
                    symbol = "✓" if status else "✗"
                    md.append(f"- {symbol} {doc_name}\n")
                md.append("\n")
            
            verification = checklist.get("verification_steps", {})
            if verification:
                md.append("### Verification Steps\n\n")
                for step_name, status in verification.items():
                    symbol = "✓" if status else "✗"
                    md.append(f"- {symbol} {step_name}\n")
                md.append("\n")
            
            readiness = checklist.get("overall_readiness", "Unknown")
            md.append(f"**Overall Readiness:** {readiness}\n\n")
    
    # Ratio Availability
    if "ratio_availability_statement" in memo_data:
        ratio_stmt = memo_data.get("ratio_availability_statement", {})
        if ratio_stmt:
            md.append("## Ratio Availability Statement\n\n")
            
            computable = ratio_stmt.get("computable_ratios", [])
            if computable:
                md.append("### Computable Ratios\n\n")
                for ratio_info in computable:
                    if isinstance(ratio_info, dict):
                        ratio_name = ratio_info.get("ratio", "")
                        ratio_value = ratio_info.get("value", "")
                        md.append(f"- **{ratio_name}:** {ratio_value}\n")
                    else:
                        md.append(f"- {str(ratio_info)}\n")
                md.append("\n")
            
            quality = ratio_stmt.get("analysis_quality", "")
            if quality:
                md.append(f"**Analysis Quality:** {quality}\n\n")
    
    # Analysis Confidence
    if "analysis_confidence" in memo_data:
        confidence = memo_data.get("analysis_confidence", {})
        if confidence:
            md.append("## Analysis Confidence Assessment\n\n")
            
            overall = confidence.get("overall_confidence_level", "Unknown")
            md.append(f"**Overall Confidence Level:** {overall}\n\n")
            
            completeness = confidence.get("completeness_score", 0)
            md.append(f"**Completeness Score:** {completeness}/100\n\n")
            
            quality = confidence.get("data_quality_assessment", "")
            if quality:
                md.append(f"**Data Quality:** {quality}\n\n")
            
            missing_count = confidence.get("missing_items_count", 0)
            md.append(f"**Missing Items:** {missing_count}\n\n")
            
            critical = confidence.get("critical_data_available", True)
            critical_text = "Yes" if critical else "No"
            md.append(f"**Critical Data Available:** {critical_text}\n\n")
    
    # Data Sources
    if "data_sources" in memo_data:
        sources = memo_data.get("data_sources", {})
        if sources:
            md.append("## Data Sources & Traceability\n\n")
            
            source_list = sources.get("sources", [])
            for source in source_list:
                if isinstance(source, dict):
                    source_text = f"{source.get('type', 'Source')}: Page {source.get('page', 'N/A')}"
                else:
                    source_text = str(source)
                md.append(f"- {source_text}\n")
            md.append("\n")
    
    # Footer
    md.append("\n---\n\n")
    md.append("*Confidential - For Authorized Use Only*\n")
    
    return "".join(md)
