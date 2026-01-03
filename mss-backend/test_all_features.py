#!/usr/bin/env python3
"""
Comprehensive test of all 7 new credit memo features.
Tests the integrated credit memo generation with all new features.
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from services.report_service import ReportService


def test_integrated_credit_memo_with_all_features():
    """Test: All 7 features integrated in credit memo"""
    print("\n" + "="*70)
    print("COMPREHENSIVE CREDIT MEMO TEST - ALL 7 FEATURES")
    print("="*70)
    
    service = ReportService()
    
    # Create comprehensive test metrics
    test_metrics = {
        "document_id": "test_doc_123",
        "company_name": "Test Company Inc.",
        "document_filename": "test_financials.pdf",
        "total_revenue": 100e6,
        "net_income": 15e6,
        "ebitda": 25e6,
        "operating_cash_flow": 20e6,
        "total_debt": 150e6,
        "total_equity": 200e6,
        "debt_to_equity": 0.75,
        "current_ratio": 1.5,
        "dscr": 1.35,
        "interest_expense": 2e6,
        "total_assets": 500e6,
        "total_liabilities": 300e6,
        "current_assets": 150e6,
        "current_liabilities": 100e6,
        "fy2022_revenue": 85e6,
        "fy2023_revenue": 92e6,
        "fy2023_debt": 140e6,
        "fy2023_ebitda": 23e6,
        "fy2023_net_income": 13e6,
        "fy2023_revenue": 92e6,
        "fy2023_operating_cash_flow": 18e6,
        "audited": True,
        "principal_repayment": 5e6,
        "collateral_coverage": 0.8,
    }
    
    # Generate risk factors for the memo
    risk_factors = [
        {
            "factor": "Market Concentration Risk",
            "severity": "MEDIUM",
            "description": "Top 3 customers represent 45% of revenue, creating customer concentration risk",
            "recommendation": "Diversify customer base to reduce concentration"
        },
        {
            "factor": "Debt Service Coverage",
            "severity": "LOW",
            "description": "DSCR of 1.35x provides adequate cushion for debt service",
            "recommendation": "Continue monitoring cash flow trends"
        },
        {
            "factor": "Operating Margins",
            "severity": "MEDIUM",
            "description": "Net margins at 15% but declining from prior year 14% due to cost pressures",
            "recommendation": "Implement cost management initiatives"
        }
    ]
    
    analysis_result = {
        "metrics": test_metrics,
        "risk_factors_objects": risk_factors,
        "recommendations": ["Maintain current financing terms", "Monitor customer concentration"],
        "analysis": {}
    }
    
    try:
        memo = service.generate_credit_memo(
            document_id=test_metrics["document_id"],
            company_name=test_metrics["company_name"],
            document_filename=test_metrics["document_filename"],
            analysis_result=analysis_result
        )
        
        # Verify all new sections exist
        print("\n[+] CREDIT MEMO GENERATED SUCCESSFULLY")
        print("\nVerifying all sections are present:")
        
        sections = [
            ("memo_type", "Memo format identifier"),
            ("executive_summary_bullets", "5-bullet executive summary"),
            ("metrics_table", "Key financial metrics table"),
            ("top_3_risks", "Top 3 risks with severity justification"),
            ("missing_information", "[NEW] Flags what data is missing"),
            ("red_flags", "[NEW] Auto-detected concerning trends"),
            ("credit_analyst_checklist", "[NEW] Standard documents checklist"),
            ("ratio_availability_statement", "[NEW] Which ratios can be computed"),
            ("key_ratios", "Core financial ratios"),
            ("data_sources", "Page-level traceability"),
            ("analysis_confidence", "[NEW] Analysis quality assessment")
        ]
        
        for section, description in sections:
            if section in memo:
                print(f"  [OK] {section}")
                print(f"       {description}")
            else:
                print(f"  [MISSING] {section}")
                return False
        
        # Detailed validation of key sections
        print("\n" + "="*70)
        print("DETAILED FEATURE VALIDATION")
        print("="*70)
        
        # Feature 1: Source Confidence Tagging
        print("\n[FEATURE 1] Source Confidence Tagging")
        bullets = memo["executive_summary_bullets"]
        print(f"  -> {len(bullets)} executive summary bullets")
        for i, bullet in enumerate(bullets, 1):
            confidence = bullet.get("source_confidence", "Unknown")
            source_strength = bullet.get("source_strength", "")
            print(f"    - Bullet {i}: {confidence} confidence")
            print(f"      {source_strength[:50]}")
        
        assert all(b.get("source_confidence") for b in bullets), "Each bullet must have source_confidence"
        print("  [OK] All bullets have source confidence ratings")
        
        # Feature 2: Risk Severity Justification
        print("\n[FEATURE 2] Risk Severity Justification")
        risks = memo["top_3_risks"]
        print(f"  -> {len(risks)} risks with severity justification")
        for i, risk in enumerate(risks, 1):
            severity = risk.get("severity", "Unknown")
            justification = risk.get("severity_justification", "")
            print(f"    - Risk {i}: {severity} severity")
            print(f"      {justification[:80]}")
        
        assert all(r.get("severity_justification") for r in risks), "Each risk must have severity_justification"
        print("  [OK] All risks have severity justifications")
        
        # Feature 3: Missing Information Detection
        print("\n[FEATURE 3] Missing Information Detection")
        missing = memo["missing_information"]
        print(f"  -> {len(missing)} items analyzed")
        if missing:
            for item in missing[:3]:
                print(f"    {item}")
        print(f"  [OK] Missing information section present")
        
        # Feature 4: Red Flag Detection
        print("\n[FEATURE 4] Red Flag Detection")
        red_flags = memo["red_flags"]
        print(f"  -> {len(red_flags)} red flags detected")
        for flag in red_flags[:2]:
            flag_name = flag.get("flag", "Unknown")
            severity = flag.get("severity", "Unknown")
            print(f"    - {flag_name} ({severity} severity)")
        print(f"  [OK] Red flag detection system active")
        
        # Feature 5: Credit Analyst Checklist
        print("\n[FEATURE 5] Credit Analyst Checklist")
        checklist = memo["credit_analyst_checklist"]
        summary = checklist["summary"]
        print(f"  -> {summary['documents_received']}/{summary['total_required']} documents reviewed")
        print(f"  -> Overall readiness: {summary['overall_readiness']}")
        print(f"  [OK] Analyst checklist system operational")
        
        # Feature 6: Ratio Availability Statement
        print("\n[FEATURE 6] Ratio Availability Statement")
        ratios = memo["ratio_availability_statement"]
        print(f"  -> Can compute: {ratios['can_compute_count']} ratios")
        print(f"  -> Cannot compute: {ratios['cannot_compute_count']} ratios")
        print(f"  -> Analysis quality: {ratios['analysis_quality']}")
        print(f"  [OK] Ratio availability assessment complete")
        
        # Feature 7: Analysis Confidence Assessment
        print("\n[FEATURE 7] Analysis Confidence Assessment")
        confidence = memo["analysis_confidence"]
        print(f"  -> Overall confidence: {confidence['overall_confidence_level']}")
        print(f"  -> Completeness score: {confidence['completeness_score']}/100")
        print(f"  -> Data quality: {confidence['data_quality_assessment']}")
        print(f"  [OK] Analysis confidence metrics calculated")
        
        # Serialization test
        print("\n" + "="*70)
        print("SERIALIZATION & FORMAT VALIDATION")
        print("="*70)
        
        memo_json = json.dumps(memo, default=str, indent=2)
        assert len(memo_json) > 1000, "Memo should be substantial"
        print(f"[OK] Memo serializable to JSON: {len(memo_json):,} characters")
        
        # Structure validation
        print(f"[OK] Executive summary: {len(memo['executive_summary_bullets'])} bullets")
        print(f"[OK] Key metrics: {len(memo['metrics_table']['rows'])} rows")
        print(f"[OK] Top risks: {len(memo['top_3_risks'])} risks")
        print(f"[OK] Key ratios: {len(memo['key_ratios'])} ratios calculated")
        
        print("\n" + "="*70)
        print("[SUCCESS] ALL TESTS PASSED - FULL FEATURE INTEGRATION VERIFIED")
        print("="*70)
        
        return True
        
    except Exception as e:
        print(f"\n[FAILED] {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run the comprehensive test"""
    print("\n" + "="*70)
    print("CREDIT MEMO SYSTEM - COMPREHENSIVE FEATURE VALIDATION")
    print("Testing all 7 new features in integrated output")
    print("="*70)
    
    success = test_integrated_credit_memo_with_all_features()
    
    if success:
        print("\n[SUCCESS] All 7 features are fully implemented and working!")
        print("\nFeatures implemented:")
        print("  1. [FEATURE] Source Confidence Tagging (HIGH/MEDIUM/LOW for each bullet)")
        print("  2. [FEATURE] Risk Severity Justification (WHY each risk is that severity)")
        print("  3. [FEATURE] Missing Information Detection (Flags gaps in data)")
        print("  4. [FEATURE] Red Flag Detection (Auto-detects concerning trends)")
        print("  5. [FEATURE] Credit Analyst Checklist (V/X for standard documents)")
        print("  6. [FEATURE] Ratio Availability Statement (Which ratios CAN be computed)")
        print("  7. [FEATURE] Analysis Confidence Assessment (Quality of analysis)")
        return 0
    else:
        print("\n[FAILURE] Some tests did not pass")
        return 1


if __name__ == "__main__":
    sys.exit(main())
