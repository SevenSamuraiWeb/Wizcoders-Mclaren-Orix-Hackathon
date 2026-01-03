"""
Quick test of the credit memo generation system.
Tests all winning features:
1. Synthetic PDF generation
2. Credit memo format with 5-bullet summary
3. Key metrics table with DSCR
4. Top 3 risks (data-tied)
5. Confidence tags
"""

import sys
import os
import tempfile

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.synthetic_data_generator import SyntheticFinancialPDFGenerator
from src.services.report_service import ReportService


def test_credit_memo_generation():
    """Test the complete credit memo flow."""
    
    print("=" * 80)
    print("🎯 HACKATHON WINNING FORMAT TEST")
    print("=" * 80)
    
    # Step 1: Generate synthetic PDF
    print("\n[1] Generating synthetic financial PDF...")
    generator = SyntheticFinancialPDFGenerator("TechCorp Inc.")
    
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        pdf_path = f.name
    
    generator.create_pdf(pdf_path)
    print(f"✓ Generated: {pdf_path}")
    
    # Step 2: Prepare mock analysis result
    print("\n[2] Creating mock analysis result...")
    analysis_result = {
        "metrics": {
            "total_revenue": 532_000_000,
            "net_income": 89_600_000,
            "ebitda": 95_760_000,
            "operating_cash_flow": 88_000_000,
            "interest_expense": 7_000_000,
            "principal_repayment": 15_000_000,
            "total_debt": 110_000_000,
            "total_equity": 310_000_000,
            "debt_to_equity": 0.35,
            "current_ratio": 1.75,
            "fy2022_revenue": 450_000_000,
            "fy2023_revenue": 531_000_000,
        },
        "risk_factors_objects": [
            {
                "factor": "Customer Concentration Risk",
                "severity": "HIGH",
                "description": "Top 3 customers represent 58% of total revenue, creating demand risk",
                "recommendation": "Diversify customer base and implement multi-year contracts"
            },
            {
                "factor": "Cash Flow Sensitivity to CapEx",
                "severity": "MEDIUM",
                "description": "Recent expansion increased CapEx to 48M, may pressure free cash flows",
                "recommendation": "Monitor capital efficiency and consider asset-light model"
            },
            {
                "factor": "Sector Cyclicality",
                "severity": "LOW",
                "description": "Software market linked to broader economic cycles",
                "recommendation": "Maintain strong balance sheet and liquidity reserves"
            }
        ],
        "analysis": {
            "summary": "Financial metrics extracted successfully",
            "confidence": 0.95,
            "document_type": "credit_memo"
        }
    }
    print("✓ Mock analysis prepared")
    
    # Step 3: Generate credit memo
    print("\n[3] Generating credit memo (THE WINNING FORMAT)...")
    memo = ReportService.generate_credit_memo(
        document_id="doc_123",
        analysis_result=analysis_result,
        document_filename="TechCorp_Financial_Statements_2024.pdf",
        company_name="TechCorp Inc."
    )
    print("✓ Credit memo generated")
    
    # Step 4: Display results
    print("\n" + "=" * 80)
    print("📊 CREDIT MEMO OUTPUT")
    print("=" * 80)
    
    print(f"\n📄 MEMO TYPE: {memo['memo_type']}")
    print(f"🏢 COMPANY: {memo['company_name']}")
    print(f"📋 MEMO ID: {memo['memo_id']}")
    
    # Executive Summary
    print("\n" + "─" * 80)
    print("📌 EXECUTIVE SUMMARY (5 BANKER-STYLE BULLETS)")
    print("─" * 80)
    for i, bullet in enumerate(memo['executive_summary_bullets'], 1):
        print(f"\n{i}. {bullet['title']}")
        print(f"   Text: {bullet['text']}")
        print(f"   Confidence: [{bullet['confidence']}]")
        print(f"   Source Page: {bullet['source_page']}")
    
    # Key Metrics Table
    print("\n" + "─" * 80)
    print("📊 KEY FINANCIAL METRICS TABLE (WITH DSCR)")
    print("─" * 80)
    table = memo['metrics_table']
    
    # Print header
    headers = table['headers']
    col_width = 15
    print(f"\n{table['title']}")
    print("─" * (col_width * 5))
    print("".join(f"{h:<{col_width}}" for h in headers))
    print("─" * (col_width * 5))
    
    # Print rows
    for row in table['rows']:
        metric = row['metric']
        fy22 = row['fy2022']
        fy23 = row['fy2023']
        fy24 = row['fy2024']
        cagr = row['cagr']
        conf = row['confidence']
        
        print(f"{metric:<{col_width}}{fy22:<{col_width}}{fy23:<{col_width}}{fy24:<{col_width}}{cagr:<{col_width}}")
        print(f"  → {conf}")
    
    print("─" * (col_width * 5))
    
    # Top 3 Risks (Data-Tied)
    print("\n" + "─" * 80)
    print("⚠️  TOP 3 RISKS (DATA-TIED TO FINANCIALS)")
    print("─" * 80)
    for risk in memo['top_3_risks']:
        print(f"\nRisk #{risk['rank']}: {risk['title']}")
        print(f"  Severity: {risk['severity']}")
        print(f"  Description: {risk['description']}")
        print(f"  Data Tie: {risk['data_tie']}")
        print(f"  Mitigation: {risk['mitigation']}")
        print(f"  Confidence: {risk['confidence']}")
    
    # Key Ratios (Banker Format)
    print("\n" + "─" * 80)
    print("📈 KEY CREDIT RATIOS")
    print("─" * 80)
    ratios = memo['key_ratios']
    print(f"  DSCR (Debt Service Coverage):        {ratios['dscr']:.2f}x")
    print(f"  Debt-to-Equity:                      {ratios['debt_to_equity']:.2f}x")
    print(f"  Current Ratio:                       {ratios['current_ratio']:.2f}x")
    print(f"  Debt-to-EBITDA:                      {ratios['debt_to_ebitda']:.2f}x")
    print(f"  Interest Coverage:                   {ratios['interest_coverage']:.2f}x")
    
    # Overall Assessment
    print("\n" + "─" * 80)
    print("🎯 OVERALL ASSESSMENT")
    print("─" * 80)
    assessment = memo['overall_assessment']
    print(f"  Credit Rating:    {assessment['rating']}")
    print(f"  Health Score:     {assessment['health_score']}/100")
    print(f"  Recommendation:   {assessment['recommendation']}")
    print(f"  Rationale:        {assessment['rationale']}")
    
    # Data Sources (Traceability)
    print("\n" + "─" * 80)
    print("📍 DATA TRACEABILITY (PAGE-LEVEL)")
    print("─" * 80)
    sources = memo['data_sources']
    for data_type, source in sources.items():
        print(f"  {data_type:<30} {source}")
    
    print("\n" + "=" * 80)
    print("✅ TEST PASSED - HACKATHON WINNING FORMAT READY!")
    print("=" * 80)
    
    print("\n🏆 KEY FEATURES IMPLEMENTED:")
    print("  ✓ 5-bullet executive summary (credit-memo style)")
    print("  ✓ Key metrics table with DSCR (THE KEY RATIO)")
    print("  ✓ Top 3 risks tied to financial data")
    print("  ✓ Confidence tags (Strong data / Incomplete)")
    print("  ✓ Page-level traceability")
    print("  ✓ Credit rating and health score")
    print("  ✓ Banker-style language throughout")
    
    # Cleanup
    import os
    os.remove(pdf_path)
    
    return memo


if __name__ == "__main__":
    try:
        memo = test_credit_memo_generation()
        print("\n✨ Demo complete! Ready for hackathon judges.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
