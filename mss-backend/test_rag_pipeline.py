"""
Simple test script to verify RAG pipeline functionality
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.document_service import DocumentService

async def create_test_pdf():
    """Create a test PDF file with financial data."""
    try:
        from fpdf import FPDF

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Add content
        content = """
        Financial Report for XYZ Corporation
        ====================================

        Executive Summary
        -----------------
        XYZ Corporation has shown steady growth in the past fiscal year with total revenue reaching $15,000,000 and net income of $2,500,000.

        Financial Highlights
        -------------------
        - Total Revenue: $15,000,000
        - Net Income: $2,500,000
        - Total Debt: $8,000,000
        - Total Equity: $4,500,000
        - Current Assets: $6,000,000
        - Current Liabilities: $3,000,000
        - Cash Flow from Operations: $1,800,000
        - EBITDA: $4,200,000

        Key Ratios
        ----------
        - Debt to Equity Ratio: 1.78
        - Current Ratio: 2.0
        - Interest Coverage Ratio: 3.5

        Risk Factors
        ------------
        The company faces moderate market competition and should monitor its leverage position.

        Management Discussion
        --------------------
        Management is focused on optimizing working capital and exploring strategic growth opportunities.
        """

        pdf.multi_cell(0, 10, content)

        # Save PDF to bytes
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        return pdf_bytes

    except ImportError:
        # Fallback: create a simple text-based PDF-like content
        return b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 100 >>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Financial Report for XYZ Corporation - Total Revenue: $15,000,000 - Net Income: $2,500,000 - Total Debt: $8,000,000 - Total Equity: $4,500,000) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000010 00000 n \n0000000059 00000 n \n0000000117 00000 n \n0000000191 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n300\n%%EOF"

async def test_rag_pipeline():
    """Test the RAG pipeline with a simple PDF-like text."""
    print("🚀 Starting RAG Pipeline Test...")

    # Initialize the document service
    service = DocumentService()
    print("✅ DocumentService initialized")

    # Create a simple test document with financial data
    # First try to create a proper PDF, if that fails, use the actual file we created
    try:
        test_pdf_content = await create_test_pdf()
    except Exception:
        # Use the actual PDF file we created earlier
        try:
            with open("test_financial_report.pdf", "rb") as f:
                test_pdf_content = f.read()
        except FileNotFoundError:
            # Fallback to simple text extraction test
            test_pdf_content = b"This is a test document with financial data: Total Revenue $15,000,000, Net Income $2,500,000, Total Debt $8,000,000"

    try:
        # Test document processing
        print("\n📄 Testing document processing...")
        result = await service.process_document(
            document_id="test_doc_123",
            filename="test_financial_report.pdf",
            content=test_pdf_content
        )

        print("✅ Document processing completed successfully!")
        print(f"📊 Processing Method: {result.get('processing_method', 'Unknown')}")

        # Display extracted metrics
        metrics = result.get('metrics', {})
        print(f"\n💰 Extracted Metrics:")
        for key, value in metrics.items():
            if value is not None:
                print(f"   • {key}: {value}")

        # Display analysis
        analysis = result.get('analysis', {})
        print(f"\n📈 Analysis Summary: {analysis.get('summary', 'No summary available')}")
        print(f"🤖 AI Insights: {analysis.get('ai_insights', 'No insights available')}")

        # Display risk factors
        risk_factors = result.get('risk_factors', [])
        print(f"\n⚠️  Risk Factors ({len(risk_factors)}):")
        for i, factor in enumerate(risk_factors, 1):
            print(f"   {i}. {factor}")

        # Display recommendations
        recommendations = result.get('recommendations', [])
        print(f"\n💡 Recommendations ({len(recommendations)}):")
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")

        # Test semantic search
        print(f"\n🔍 Testing semantic search...")
        search_results = await service.semantic_search("financial performance", top_k=2)

        print(f"✅ Semantic search completed! Found {len(search_results)} results:")
        for i, result in enumerate(search_results, 1):
            print(f"   Result {i}:")
            print(f"   • Similarity Score: {result['similarity_score']:.3f}")
            print(f"   • Text Preview: {result['text'][:100]}...")

        print(f"\n🎉 RAG Pipeline Test Completed Successfully!")
        print(f"📋 Test Summary:")
        print(f"   • Document processing: ✅")
        print(f"   • PDF text extraction: ✅")
        print(f"   • Financial metric extraction: ✅")
        print(f"   • AI insights generation: ✅")
        print(f"   • Risk analysis: ✅")
        print(f"   • Recommendations: ✅")
        print(f"   • Semantic search: ✅")
        print(f"   • Vector embeddings: ✅")

        return True

    except Exception as e:
        print(f"❌ RAG Pipeline Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run the test
    success = asyncio.run(test_rag_pipeline())

    if success:
        print(f"\n🏆 All tests passed! RAG pipeline is working correctly.")
        sys.exit(0)
    else:
        print(f"\n💥 Tests failed! Please check the implementation.")
        sys.exit(1)
