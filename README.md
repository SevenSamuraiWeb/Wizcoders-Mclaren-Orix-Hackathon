# AI-Powered Credit Memo Generator

**Hackathon:** McLaren Strategic Solutions × Orixx Hackathon

---

## Project Overview

Credit analysts at banks spend 4–8 hours manually reviewing audited financial statements, extracting key metrics, identifying risks, and synthesizing findings into a credit memo. This process is inherently slow, prone to human error, and creates audit trails that are difficult to reconstruct when decisions are challenged.

The **AI-Powered Credit Memo Generator** transforms this workflow. By combining PDF ingestion, semantic embeddings, and retrieval-augmented generation (RAG), the system automatically extracts evidence-backed insights from financial PDFs and generates structured, citation-rich credit memos ready for analyst review and executive sign-off. Every claim is traceable to a specific page, every insight is grounded in source data, and every decision is defensible.

This is not a chatbot. This is a decision-support tool built for the banking industry—where explainability, auditability, and trust are non-negotiable.

---

## Why This Matters: Business Impact

**Auditability & Compliance**  
In banking, every credit decision must be justified and auditable. Traditional systems create untracked analysis; this system generates immutable, page-linked evidence trails. Regulators see exactly which documents informed which conclusions.

**Time & Cost Savings**  
A typical credit memo takes 4–8 analyst hours. This system reduces that to 30 minutes of human review. For a mid-size bank processing 50+ credit decisions monthly, that translates to 150+ analyst-hours freed annually—redirected toward high-touch relationship management and complex deals.

**Risk Reduction**  
Manual extraction introduces transcription errors, missed red flags, and inconsistent analysis quality. A semantic retrieval system catches contextual nuances humans overlook and enforces consistency across portfolios. Confidence scoring surfaces where analysis is weak and requires deeper investigation.

**Decision Readiness**  
Credit executives need memos they can sign without rewrites. By structuring output to banking standards (executive summary, financials, risks, recommendation), this system delivers analyst-quality work on first pass.

---

## Key Features

- **PDF Text & Table Extraction** – Parses financial PDFs page-by-page using PyMuPDF and pdfplumber; preserves page references
- **Topic-Based Retrieval** – Searches extracted content by financial topic (revenue, risks, cash flow, etc.) to gather context
- **5Cs Credit Analysis** – Generates structured analysis across Character, Capacity, Capital, Collateral, and Conditions
- **Structured Credit Memo Output** – Executive Summary, Financial Metrics, 5Cs Analysis, Risk Assessment, formatted for banking review
- **JSON & Word Export** – Generates machine-readable JSON and downloadable Word documents (.docx)
- **Streamlit & FastAPI Interfaces** – Web UI for interactive analysis and REST API for programmatic integration

---

## System Architecture

```
PDF Upload
    ↓
[PDF Parser] → Extract text & tables from each page (PyMuPDF + pdfplumber)
    ↓
[Content Retriever] → Search extracted text by financial topic (revenue, risks, cash flow, etc.)
    ↓
[LLM Prompting] → Groq API with retrieved context + structured instructions
    ↓
[Credit Memo Generator] → Builds structured analysis:
   - Executive Summary
   - Financial Metrics
   - 5Cs Analysis (Character, Capacity, Capital, Collateral, Conditions)
   - Risk Assessment
    ↓
[Output Formatting] → JSON structure, Word document (.docx), Markdown
    ↓
[User Interfaces] → Streamlit (interactive) + FastAPI (REST API)
```
---

## Retrieval & Analysis Approach

### Topic-Based Content Retrieval

Instead of free-form semantic search, the system uses predefined topic queries to pull relevant sections from the financial statements:
- **Executive Summary** → Revenue, profitability, cash flow
- **Financial Metrics** → Balance sheet, income statement figures
- **Cash Flow Analysis** → Operating, investing, financing cash flows
- **Risk Assessment** → Borrowings, liabilities, contingencies
- **Recommendation** → Overall financial position, repayment capacity

Each section query returns matching pages and extracted text, which is passed directly to the LLM.

### LLM-Driven Analysis

The Groq LLM receives:
1. The retrieved text context from specified pages
2. Structured instructions for analysis (5Cs framework, banking metrics, risks)
3. Explicit instruction to ground all analysis in provided content

The LLM generates responses formatted as JSON, making outputs machine-readable and easily validated by analysts.

### Auditability

The memo preserves:
- Page numbers where information was sourced
- Which topics were searched for each section
- The full context passed to the LLM
- Metadata: document name, pages analyzed, processing time, model used

---

## Credit Memo Structure

Credit memos in banking follow a standardized structure to ensure consistency and rapid executive comprehension:

**Executive Summary** (~300 words)
- Company overview, loan purpose, risk profile, recommendation
- Analyst sees this first; sets the decision tone

**Financial Overview**
- Key metrics: Revenue, EBITDA, leverage, interest coverage
- Sourced from P&L and balance sheet analysis
- 3-year trend (if available)

**Risk Assessment**
- Operational risks: Industry headwinds, management depth, customer concentration
- Financial risks: Debt covenants, working capital trends, capital structure
- Mitigants: Cash reserves, hedges, strategic assets
- Each risk cites source pages

**Recommendation**
- Approve / Conditional Approval / Decline
- Recommended facility size and pricing
- Key covenants and monitoring points
- Specific pages from financials supporting the decision

**Sources**
- Hyperlinked list of all cited pages
- Quick jump to evidence

This structure matches real banking practice (JPMorgan, Goldman Sachs, Bank of America templates). Judges recognize it immediately; banks can plug it directly into their workflows.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|--------|
| **PDF Processing** | PyMuPDF (fitz), pdfplumber | Extract text and tables page-by-page |
| **Content Retrieval** | Keyword-based search | Match financial topics to extracted pages |
| **LLM** | Groq API (LLaMA) | Generate structured credit analysis from retrieved context |
| **Output Formatting** | python-docx, JSON | Generate Word documents and machine-readable JSON |
| **Backend APIs** | Python, FastAPI | REST API for programmatic access |
| **Interactive UI** | Streamlit | Web interface for document upload and analysis review |
| **Frontend** | React, Vite | User dashboard (development in progress) |

---

## How to Run Locally

### Prerequisites

- Python 3.9+
- Node.js 16+
- pip and npm

### Backend Setup

```bash
cd mss-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_key_here  # or Grok API key
export FAISS_INDEX_PATH=./vector_store.index

# Start the API server
python api.py
# Server runs on http://localhost:8000
```

### Frontend Setup

```bash
cd mss-frontend
npm install
npm run dev
# Frontend runs on http://localhost:5173
```

### First Run

1. Open http://localhost:5173 in your browser
2. Use the File Upload component to ingest a PDF financial statement (sample available in `docs/sample_financial_statement.pdf`)
3. System automatically:
   - Extracts pages
   - Generates embeddings
   - Stores vectors in FAISS
   - Indexes becomes searchable
4. Navigate to Dashboard → Credit Memo → Review and Download

### Optional: API Testing

```bash
# Test health check
curl http://localhost:8000/health

# Upload a PDF
curl -F "file=@path/to/statement.pdf" http://localhost:8000/upload

# Generate memo
curl -X POST http://localhost:8000/generate_memo \
  -H "Content-Type: application/json" \
  -d '{"pdf_id": "statement_001", "analysis_type": "credit"}'
```

---

## Demo Walkthrough

1. **PDF Upload** 
   - System extracts text and tables, displays page count

2. **Topic-Based Retrieval** – System pulls relevant sections:
   - Financial metrics from balance sheets and income statements
   - Risk factors from footnotes and management discussion
   - Cash flow information from cash flow statements

3. **Credit Memo Generation** – LLM analyzes retrieved content and generates:
   - Executive Summary with recommendation
   - Key Financial Metrics
   - 5Cs Credit Analysis (Character, Capacity, Capital, Collateral, Conditions)
   - Risk Assessment
   - Source page citations throughout

4. **Output Review**
   - Formatted memo in Streamlit interface
   - JSON export with structured data
   - Word document (.docx) for distribution

5. **API Access** 
   - Upload PDF via multipart request
   - Trigger memo generation
   - Retrieve JSON results programmatically

**Time:** ~1–2 minutes from upload to final memo, depending on document length.

---

## Innovation & Differentiation

**Banking-Specific, Not Generic Chat**

- Unlike ChatPDF or generic document search, this system generates **structured credit memos** following banking industry standards (5Cs framework).
- Output is immediately usable for loan approval decisions, not conversational Q&A.

**Reproducible Analysis**

- Every memo includes metadata: which pages were analyzed, what topics were searched, which LLM model generated findings.
- Analysts and auditors can trace findings back to source documents.

**Page-Aware Extraction**

- The system explicitly tracks which pages contain financial data, rather than treating PDFs as unstructured text.
- Banks get page numbers with every insight, enabling rapid verification.

**Structured Output**

- JSON format enables integration with loan management systems, CRM, and document repositories.
- Word export allows immediate distribution to credit committees.
- No free-form text that requires re-entry into banking systems.

**LLM-Powered Without Hallucination Risk**

- By passing only retrieved document content to the LLM (no external knowledge), false claims are minimized.
- LLM generates prose from structured financial data—similar to human analyst synthesis.
- Memos are reviewed by analysts before approval (by design, for compliance).

---

### Future Enhancements

1. **Multi-Year Analysis** – Support uploading 3–5 years of audited statements; auto-generate trend analysis (revenue growth, leverage improvement, etc.).
2. **Peer Benchmarking** – Compare key metrics (debt-to-equity, interest coverage) against industry peers (pulled from public data / proprietary databases).
3. **Enhanced Table Recognition** – Improve extraction of complex financial statement tables using OCR or table detection models.
4. **Covenant Monitoring** – Track loan covenants over time; flag when near violation thresholds.
5. **Sensitivity Analysis** – "What if revenue drops 20%? What's the new leverage ratio?"
6. **Fine-Tuned LLM** – Retrain Groq model on proprietary credit memo examples for improved banking terminology and analysis depth.

---

## Team & Acknowledgements

**Project Team:** Wizcoders for McLaren Strategic Solutions × Orixx Hackathon

*
