# 🏆 Wizcoders-Mclaren-Orix Hackathon: AI Credit Analyst

## Overview

This is a **banker-style credit analysis system** built for the hackathon. It's NOT a generic document summarizer - it's an AI junior credit analyst that generates professional-grade credit memoranda.

### What Makes This Different

| Feature | Generic Summarizer | Your System |
|---------|-------------------|------------|
| **Output** | Paragraphs | Structured credit memo |
| **Key Metric** | None | DSCR (what bankers use) |
| **Risk Analysis** | Generic | Data-tied (e.g., "Top 3 customers = 58%") |
| **Confidence** | Black box | Tagged (Strong/Incomplete data) |
| **Traceability** | None | Page-level source tracking |
| **Language** | ChatGPT-style | Banker terminology |

---

## 🚀 Quick Start

### Windows
```bash
cd path\to\Wizcoders-Mclaren-Orix-Hackathon
QUICK_SETUP.bat
```

### Linux/Mac
```bash
cd path/to/Wizcoders-Mclaren-Orix-Hackathon
bash QUICK_SETUP.sh
```

### Manual Setup
```bash
cd mss-backend
pip install -r requirements.txt
pip install reportlab==4.0.9
python test_credit_memo.py
```

---

## 📊 What You Get

### 1. **Synthetic Financial PDFs**
- Multi-year statements (FY22, FY23, FY24)
- Income Statement, Balance Sheet, Cash Flow
- Realistic financial data
- File: `tests/synthetic_data_generator.py`

### 2. **Credit Memorandum Generator**
- **5-Bullet Executive Summary** (credit-memo style)
- **Key Metrics Table** (3-year history with CAGR)
- **Top 3 Risks** (data-tied to financial metrics)
- **DSCR Calculation** (Debt Service Coverage Ratio)
- **Overall Assessment** (Credit rating A-BBB-, health score)
- **Confidence Tags** (Strong data vs. Incomplete)
- **Page-Level Traceability** (source for every insight)

### 3. **API Endpoints**
```
POST /api/v1/documents/upload
        Upload PDF for analysis

GET /api/v1/documents/{doc_id}/credit-memo
        Get full credit memo (JSON)

POST /api/v1/documents/{doc_id}/simplify-text
        Simplify financial language for non-finance audience

GET /api/v1/documents/{doc_id}/report
GET /api/v1/documents/{doc_id}/report/json
GET /api/v1/documents/{doc_id}/report/html
        Alternative report formats
```

---

## 🎯 Demo Flow (For Judges)

### Step 1: Upload PDF
```bash
curl -X POST http://localhost:8001/api/v1/documents/upload \
  -F "file=@financial_statements.pdf"
```

### Step 2: Get Credit Memo
```bash
curl http://localhost:8001/api/v1/documents/{doc_id}/credit-memo
```

### Step 3: See the Output
The response includes:
- 5-bullet summary with DSCR
- Key metrics table (FY22/23/24)
- Top 3 risks with data ties
- Credit rating and health score
- Page-level traceability

---

## 📁 Project Structure

```
Wizcoders-Mclaren-Orix-Hackathon/
├── docs/
│   ├── HACKATHON_DEMO_GUIDE.md      ← Read this for 2-min pitch
│   ├── IMPLEMENTATION_SUMMARY.md    ← Technical details
│   └── ...
├── mss-backend/
│   ├── src/
│   │   ├── services/
│   │   │   ├── report_service.py    ← Credit memo generation
│   │   │   ├── document_service.py  ← PDF processing + simplify_text()
│   │   │   └── ...
│   │   ├── api/v1/
│   │   │   ├── documents.py         ← /credit-memo endpoints
│   │   │   └── ...
│   │   └── main.py
│   ├── tests/
│   │   ├── synthetic_data_generator.py  ← Generates test PDFs
│   │   └── ...
│   ├── test_credit_memo.py          ← Run this to test
│   ├── requirements.txt
│   └── ...
├── mss-frontend/
│   └── ... (React frontend)
├── QUICK_SETUP.bat                   ← Windows setup
├── QUICK_SETUP.sh                    ← Linux/Mac setup
└── README.md
```

---

## 🔑 Key Components

### 1. ReportService.generate_credit_memo()
Generates banker-style credit memo with:
```python
{
    "executive_summary_bullets": [
        {
            "title": "Business Performance Trend",
            "text": "Revenue grew at 14% CAGR...",
            "confidence": "Strong data",
            "source_page": 1
        },
        ...
    ],
    "metrics_table": {
        "rows": [
            {"metric": "DSCR", "fy2024": "1.86x", "confidence": "Strong data"},
            ...
        ]
    },
    "top_3_risks": [
        {
            "title": "Customer Concentration",
            "severity": "HIGH",
            "description": "Top 3 customers = 58% of revenue",
            "data_tie": "58%",
            "source_page": 3
        },
        ...
    ],
    "overall_assessment": {
        "rating": "A (Strong)",
        "health_score": 78,
        "recommendation": "APPROVE"
    }
}
```

### 2. DSCR Calculation
```python
DSCR = Operating Cash Flow / (Principal + Interest)

Interpretation:
  ≥1.5x: Excellent  (strong debt service capability)
  ≥1.25x: Strong    (adequate debt coverage)
  ≥1.0x: Adequate   (can service debt)
  <1.0x: Concerning (may struggle)
```

### 3. Credit Rating Formula
- Based on DSCR (40%)
- Leverage/Debt-to-Equity (35%)
- Risk profile (25%)
- Outputs: A+, A, BBB+, BBB, BBB-

### 4. Synthetic PDF Generator
Generates realistic financial statements:
```python
generator = SyntheticFinancialPDFGenerator("Company Name")
generator.create_pdf("output.pdf")
```

---

## 💡 Why This Wins Hackathons

### Domain Knowledge
✅ DSCR (shows credit analysis expertise)
✅ Banker terminology (leverage, liquidity, debt service)
✅ 3-year trends (not just snapshots)
✅ Risk data-tying (58%, $48M)
✅ Credit ratings (A, BBB framework)

### User Experience
✅ Structured output (not prose)
✅ Confidence tags (data quality)
✅ Page traceability (auditable)
✅ Text simplification (human-in-loop)

### Presentation
✅ Looks like a real bank product
✅ Not generic AI summary
✅ Domain-specific language
✅ Professional formatting

---

## 🧪 Testing

### Run Credit Memo Test
```bash
cd mss-backend
python test_credit_memo.py
```

Output shows:
- Executive summary (5 bullets)
- Key metrics table (with DSCR)
- Top 3 risks (data-tied)
- Overall assessment
- Key ratios

### Test API Endpoint
```bash
# Start backend
uvicorn src.main:app --reload --port 8001

# In another terminal
curl http://localhost:8001/api/v1/documents/doc_123/credit-memo
```

---

## 📋 Files Added/Modified

### Created
- `tests/synthetic_data_generator.py` - Synthetic PDF generator
- `test_credit_memo.py` - Credit memo test
- `docs/HACKATHON_DEMO_GUIDE.md` - Judge demo guide
- `docs/IMPLEMENTATION_SUMMARY.md` - Technical summary
- `QUICK_SETUP.bat` / `QUICK_SETUP.sh` - Setup scripts

### Modified
- `src/services/report_service.py` - Added `generate_credit_memo()` + helpers
- `src/services/document_service.py` - Added `simplify_text()` method
- `src/api/v1/documents.py` - Added `/credit-memo` + `/simplify-text` endpoints
- `requirements.txt` - Added `reportlab==4.0.9`

---

## 🎓 2-Minute Judge Pitch

```
"We built an AI junior credit analyst - not a document summarizer.

This generates credit memoranda: structured output that looks like what 
a bank would circulate internally.

Key features:
- 5 banker-style bullets (not generic AI summary)
- Key metrics table with DSCR (debt service coverage ratio)
- Top 3 risks tied to actual financial data (e.g., 'Top 3 customers = 58%')
- Page-level traceability (not a black box)
- Confidence tags (shows understanding of data quality)

The DSCR at 1.86x means they make 1.86 times their annual debt payments - excellent.
Combined with moderate leverage (0.35x), we rate them 'A (Strong)'.

This doesn't compete on better ML. It competes on better domain understanding.
That's how you beat teams with superior algorithms."
```

---

## 🚦 Traffic Light Status

✅ **GREEN** - Production ready
- Credit memo generation ✓
- DSCR calculation ✓
- Confidence tags ✓
- API endpoints ✓
- Test suite ✓

🟡 **YELLOW** - Nice to have (if time allows)
- PDF export (banker format)
- Batch processing
- Year-over-year comparison

🔴 **RED** - Advanced features
- Industry benchmarking
- Covenant checking
- Trend analysis

---

## 📞 Support

### Setup Issues
- Windows: Run `QUICK_SETUP.bat`
- Linux/Mac: Run `QUICK_SETUP.sh`
- Manual: See instructions above

### Test Issues
```bash
# Check dependencies
pip list | grep -E "reportlab|fastapi|pydantic|sentence-transformers|faiss"

# Reinstall specific dependency
pip install reportlab==4.0.9 --force-reinstall
```

### Demo Issues
1. Check backend is running: `http://localhost:8001/api/v1/health/status`
2. Check frontend is running: `http://localhost:5173`
3. Try sample upload from `HACKATHON_DEMO_GUIDE.md`

---

## 🏆 Good Luck!

This system is built to win because it shows:
1. **Domain knowledge** (credit analysis terminology)
2. **Thoughtful design** (structured output, not prose)
3. **User awareness** (confidence tags, traceability)
4. **Professional execution** (banker-grade language)

Go show those judges! 🚀

---

**Last Updated**: January 3, 2026
**Status**: Production Ready ✅
