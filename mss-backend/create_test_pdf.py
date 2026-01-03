"""
Create a test PDF file for RAG pipeline testing
"""

from fpdf import FPDF
import os

def create_test_pdf():
    """Create a test PDF file with financial data."""
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

    # Save PDF
    pdf_path = "test_financial_report.pdf"
    pdf.output(pdf_path)

    print(f"✅ Test PDF created: {pdf_path}")
    print(f"📄 File size: {os.path.getsize(pdf_path)} bytes")

    return pdf_path

if __name__ == "__main__":
    create_test_pdf()
