"""
Synthetic Financial PDF Generator

Creates realistic test PDFs with multi-year financial statements
for hackathon demo purposes.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from datetime import datetime
import random


class SyntheticFinancialPDFGenerator:
    """Generate synthetic financial PDFs with multi-year statements."""

    def __init__(self, company_name="TechCorp Inc."):
        self.company_name = company_name
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a3a52'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        self.styles.add(ParagraphStyle(
            name='TableHeading',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.white,
            fontName='Helvetica-Bold',
            alignment='CENTER'
        ))

    def generate_financial_data(self) -> dict:
        """
        Generate realistic multi-year financial data (FY22, FY23, FY24).
        
        Returns:
            Dictionary with income statement, balance sheet, and cash flow data
        """
        # Income Statement
        fy22_revenue = 450_000_000
        fy23_revenue = fy22_revenue * 1.18  # 18% growth
        fy24_revenue = fy23_revenue * 1.14  # 14% growth

        data = {
            # Income Statement
            "income_statement": {
                "FY2022": {
                    "revenue": fy22_revenue,
                    "cost_of_revenue": fy22_revenue * 0.65,
                    "gross_profit": fy22_revenue * 0.35,
                    "operating_expenses": fy22_revenue * 0.22,
                    "ebitda": fy22_revenue * 0.13,
                    "depreciation": fy22_revenue * 0.03,
                    "ebit": fy22_revenue * 0.10,
                    "interest_expense": 8_000_000,
                    "tax": (fy22_revenue * 0.10 - 8_000_000) * 0.25,
                    "net_income": (fy22_revenue * 0.10 - 8_000_000) * 0.75,
                },
                "FY2023": {
                    "revenue": fy23_revenue,
                    "cost_of_revenue": fy23_revenue * 0.64,
                    "gross_profit": fy23_revenue * 0.36,
                    "operating_expenses": fy23_revenue * 0.20,
                    "ebitda": fy23_revenue * 0.16,
                    "depreciation": fy23_revenue * 0.03,
                    "ebit": fy23_revenue * 0.13,
                    "interest_expense": 7_500_000,
                    "tax": (fy23_revenue * 0.13 - 7_500_000) * 0.25,
                    "net_income": (fy23_revenue * 0.13 - 7_500_000) * 0.75,
                },
                "FY2024": {
                    "revenue": fy24_revenue,
                    "cost_of_revenue": fy24_revenue * 0.63,
                    "gross_profit": fy24_revenue * 0.37,
                    "operating_expenses": fy24_revenue * 0.19,
                    "ebitda": fy24_revenue * 0.18,
                    "depreciation": fy24_revenue * 0.03,
                    "ebit": fy24_revenue * 0.15,
                    "interest_expense": 7_000_000,
                    "tax": (fy24_revenue * 0.15 - 7_000_000) * 0.25,
                    "net_income": (fy24_revenue * 0.15 - 7_000_000) * 0.75,
                },
            },
            # Balance Sheet
            "balance_sheet": {
                "FY2022": {
                    "current_assets": 180_000_000,
                    "ppe": 220_000_000,
                    "total_assets": 400_000_000,
                    "current_liabilities": 120_000_000,
                    "long_term_debt": 130_000_000,
                    "total_debt": 130_000_000,
                    "total_liabilities": 250_000_000,
                    "total_equity": 150_000_000,
                },
                "FY2023": {
                    "current_assets": 220_000_000,
                    "ppe": 260_000_000,
                    "total_assets": 480_000_000,
                    "current_liabilities": 140_000_000,
                    "long_term_debt": 125_000_000,
                    "total_debt": 125_000_000,
                    "total_liabilities": 265_000_000,
                    "total_equity": 215_000_000,
                },
                "FY2024": {
                    "current_assets": 280_000_000,
                    "ppe": 300_000_000,
                    "total_assets": 580_000_000,
                    "current_liabilities": 160_000_000,
                    "long_term_debt": 110_000_000,
                    "total_debt": 110_000_000,
                    "total_liabilities": 270_000_000,
                    "total_equity": 310_000_000,
                },
            },
            # Cash Flow Statement
            "cash_flow": {
                "FY2022": {
                    "operating_cash_flow": 62_000_000,
                    "capex": 35_000_000,
                    "free_cash_flow": 27_000_000,
                    "debt_repayment": 5_000_000,
                },
                "FY2023": {
                    "operating_cash_flow": 75_000_000,
                    "capex": 42_000_000,
                    "free_cash_flow": 33_000_000,
                    "debt_repayment": 5_000_000,
                },
                "FY2024": {
                    "operating_cash_flow": 88_000_000,
                    "capex": 48_000_000,
                    "free_cash_flow": 40_000_000,
                    "debt_repayment": 15_000_000,
                },
            },
        }

        return data

    def create_pdf(self, output_path: str) -> str:
        """
        Create a synthetic financial PDF and save to disk.

        Args:
            output_path: Path where PDF should be saved

        Returns:
            Path to created PDF
        """
        doc = SimpleDocTemplate(output_path, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []

        # Generate data
        data = self.generate_financial_data()

        # Title
        story.append(Paragraph(f"<b>{self.company_name}</b>", self.styles['CustomTitle']))
        story.append(Paragraph(f"Financial Statements and Credit Analysis", self.styles['Heading2']))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))

        # ===== INCOME STATEMENT =====
        story.append(Paragraph("<b>1. INCOME STATEMENT (In USD Millions)</b>", self.styles['Heading2']))
        income_table_data = [
            ["Item", "FY2022", "FY2023", "FY2024"],
            ["Total Revenue", f"${data['income_statement']['FY2022']['revenue']/1e6:.1f}M",
             f"${data['income_statement']['FY2023']['revenue']/1e6:.1f}M",
             f"${data['income_statement']['FY2024']['revenue']/1e6:.1f}M"],
            ["Cost of Revenue", f"${data['income_statement']['FY2022']['cost_of_revenue']/1e6:.1f}M",
             f"${data['income_statement']['FY2023']['cost_of_revenue']/1e6:.1f}M",
             f"${data['income_statement']['FY2024']['cost_of_revenue']/1e6:.1f}M"],
            ["Gross Profit", f"${data['income_statement']['FY2022']['gross_profit']/1e6:.1f}M",
             f"${data['income_statement']['FY2023']['gross_profit']/1e6:.1f}M",
             f"${data['income_statement']['FY2024']['gross_profit']/1e6:.1f}M"],
            ["Operating Expenses", f"${data['income_statement']['FY2022']['operating_expenses']/1e6:.1f}M",
             f"${data['income_statement']['FY2023']['operating_expenses']/1e6:.1f}M",
             f"${data['income_statement']['FY2024']['operating_expenses']/1e6:.1f}M"],
            ["EBITDA", f"${data['income_statement']['FY2022']['ebitda']/1e6:.1f}M",
             f"${data['income_statement']['FY2023']['ebitda']/1e6:.1f}M",
             f"${data['income_statement']['FY2024']['ebitda']/1e6:.1f}M"],
            ["EBITDA Margin %", f"{(data['income_statement']['FY2022']['ebitda']/data['income_statement']['FY2022']['revenue']*100):.1f}%",
             f"{(data['income_statement']['FY2023']['ebitda']/data['income_statement']['FY2023']['revenue']*100):.1f}%",
             f"{(data['income_statement']['FY2024']['ebitda']/data['income_statement']['FY2024']['revenue']*100):.1f}%"],
            ["Depreciation", f"${data['income_statement']['FY2022']['depreciation']/1e6:.1f}M",
             f"${data['income_statement']['FY2023']['depreciation']/1e6:.1f}M",
             f"${data['income_statement']['FY2024']['depreciation']/1e6:.1f}M"],
            ["EBIT", f"${data['income_statement']['FY2022']['ebit']/1e6:.1f}M",
             f"${data['income_statement']['FY2023']['ebit']/1e6:.1f}M",
             f"${data['income_statement']['FY2024']['ebit']/1e6:.1f}M"],
            ["Interest Expense", f"${data['income_statement']['FY2022']['interest_expense']/1e6:.1f}M",
             f"${data['income_statement']['FY2023']['interest_expense']/1e6:.1f}M",
             f"${data['income_statement']['FY2024']['interest_expense']/1e6:.1f}M"],
            ["Net Income", f"${data['income_statement']['FY2022']['net_income']/1e6:.1f}M",
             f"${data['income_statement']['FY2023']['net_income']/1e6:.1f}M",
             f"${data['income_statement']['FY2024']['net_income']/1e6:.1f}M"],
        ]

        income_table = Table(income_table_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        income_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a52')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(income_table)
        story.append(Spacer(1, 0.2*inch))

        # ===== BALANCE SHEET =====
        story.append(Paragraph("<b>2. BALANCE SHEET (In USD Millions)</b>", self.styles['Heading2']))
        bs_table_data = [
            ["Item", "FY2022", "FY2023", "FY2024"],
            ["Current Assets", f"${data['balance_sheet']['FY2022']['current_assets']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2023']['current_assets']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2024']['current_assets']/1e6:.1f}M"],
            ["PPE", f"${data['balance_sheet']['FY2022']['ppe']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2023']['ppe']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2024']['ppe']/1e6:.1f}M"],
            ["Total Assets", f"${data['balance_sheet']['FY2022']['total_assets']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2023']['total_assets']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2024']['total_assets']/1e6:.1f}M"],
            ["Current Liabilities", f"${data['balance_sheet']['FY2022']['current_liabilities']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2023']['current_liabilities']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2024']['current_liabilities']/1e6:.1f}M"],
            ["Long-term Debt", f"${data['balance_sheet']['FY2022']['long_term_debt']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2023']['long_term_debt']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2024']['long_term_debt']/1e6:.1f}M"],
            ["Total Debt", f"${data['balance_sheet']['FY2022']['total_debt']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2023']['total_debt']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2024']['total_debt']/1e6:.1f}M"],
            ["Total Equity", f"${data['balance_sheet']['FY2022']['total_equity']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2023']['total_equity']/1e6:.1f}M",
             f"${data['balance_sheet']['FY2024']['total_equity']/1e6:.1f}M"],
            ["Debt/Equity Ratio", f"{data['balance_sheet']['FY2022']['total_debt']/data['balance_sheet']['FY2022']['total_equity']:.2f}x",
             f"{data['balance_sheet']['FY2023']['total_debt']/data['balance_sheet']['FY2023']['total_equity']:.2f}x",
             f"{data['balance_sheet']['FY2024']['total_debt']/data['balance_sheet']['FY2024']['total_equity']:.2f}x"],
        ]

        bs_table = Table(bs_table_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        bs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a52')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(bs_table)
        story.append(Spacer(1, 0.2*inch))

        # ===== CASH FLOW =====
        story.append(Paragraph("<b>3. CASH FLOW STATEMENT (In USD Millions)</b>", self.styles['Heading2']))
        cf_table_data = [
            ["Item", "FY2022", "FY2023", "FY2024"],
            ["Operating Cash Flow", f"${data['cash_flow']['FY2022']['operating_cash_flow']/1e6:.1f}M",
             f"${data['cash_flow']['FY2023']['operating_cash_flow']/1e6:.1f}M",
             f"${data['cash_flow']['FY2024']['operating_cash_flow']/1e6:.1f}M"],
            ["Capital Expenditures", f"${data['cash_flow']['FY2022']['capex']/1e6:.1f}M",
             f"${data['cash_flow']['FY2023']['capex']/1e6:.1f}M",
             f"${data['cash_flow']['FY2024']['capex']/1e6:.1f}M"],
            ["Free Cash Flow", f"${data['cash_flow']['FY2022']['free_cash_flow']/1e6:.1f}M",
             f"${data['cash_flow']['FY2023']['free_cash_flow']/1e6:.1f}M",
             f"${data['cash_flow']['FY2024']['free_cash_flow']/1e6:.1f}M"],
            ["Debt Repayment", f"${data['cash_flow']['FY2022']['debt_repayment']/1e6:.1f}M",
             f"${data['cash_flow']['FY2023']['debt_repayment']/1e6:.1f}M",
             f"${data['cash_flow']['FY2024']['debt_repayment']/1e6:.1f}M"],
        ]

        cf_table = Table(cf_table_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        cf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a3a52')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(cf_table)
        story.append(Spacer(1, 0.2*inch))

        # ===== NOTES TO FINANCIAL STATEMENTS =====
        story.append(PageBreak())
        story.append(Paragraph("<b>4. NOTES TO FINANCIAL STATEMENTS</b>", self.styles['Heading2']))
        
        notes = [
            "<b>Company Overview:</b> TechCorp Inc. is a leading provider of enterprise software solutions with operations across North America, Europe, and Asia. The company serves over 500 enterprise customers.",
            "",
            "<b>Significant Accounting Policies:</b> Financial statements are prepared in accordance with GAAP. Revenue is recognized upon delivery of services. The company uses the straight-line method for depreciation over 7 years.",
            "",
            "<b>Credit Facilities:</b> The company has access to a $200M revolving credit facility at LIBOR + 2.5%. As of FY2024, $90M is drawn. The facility matures in 2026.",
            "",
            "<b>Debt Covenants:</b> The company is required to maintain a Debt/EBITDA ratio below 1.5x and an interest coverage ratio above 4.0x. Current ratios are 0.85x and 15.5x respectively.",
            "",
            "<b>Contingent Liabilities:</b> The company is subject to ongoing litigation related to product liability claims. Management estimates potential exposure at $5-10M. No accrual has been recorded.",
        ]
        
        for note in notes:
            if note:
                story.append(Paragraph(note, self.styles['Normal']))
                story.append(Spacer(1, 0.1*inch))

        # Build PDF
        doc.build(story)
        return output_path


# Test function
if __name__ == "__main__":
    generator = SyntheticFinancialPDFGenerator("TechCorp Inc.")
    output_path = "/tmp/synthetic_financial_report.pdf"
    generator.create_pdf(output_path)
    print(f"✓ Generated synthetic PDF: {output_path}")
