# Architecture: AI-Powered Credit Memo Generator

## System Overview

The AI Credit Memo Generator is a document processing pipeline that ingests financial statement PDFs, extracts structured financial data, and generates banking-grade credit memos with LLM-driven analysis. The system prioritizes **auditability**, **reproducibility**, and **source attribution** over raw speed or complexity.

```
[PDF Upload] → [Extraction] → [Topic-Based Retrieval] → [LLM Analysis] → [Structured Output]
     ↓              ↓                 ↓                      ↓              ↓
  Streamlit    PDF Parser      Context Retriever      Groq LLM       JSON/DOCX/Markdown
  FastAPI      (PyMuPDF)       (Keyword Search)     (LLaMA 2/Scout)   + Metadata
```

---

## Component Breakdown

### 1. PDF Parser (`pdf_processor.py`)

**Purpose:** Extract text and tables from financial statement PDFs while preserving page-level metadata.

**Implementation:**
- **PyMuPDF (fitz)** – Fast page-by-page text extraction
- **pdfplumber** – Precise table extraction with cell content preservation

**Key Design:**
```python
class PDFProcessor:
    def parse(self) -> list[dict]:
        """Returns list of page objects with page number, text, and tables."""
        text_data = self._extract_text_with_fitz()
        table_data = self._extract_tables_with_plumber()
        # Merge by page index, preserving page numbers
        return merged_pages
```

**Output Format:**
```json
[
  {
    "page": 1,
    "text": "Statement of Financial Position...",
    "tables": [
      [["Assets", "2024", "2023"], ["Cash", "1M", "0.8M"], ...]
    ]
  }
]
```

**Why This Approach:**
- Page numbers are preserved from extraction, not recovered later
- Tables are extracted structurally (not as OCR images), enabling downstream parsing
- Separate text and table extraction allows fallback if one fails
- No chunking or embedding loss at this stage

**Trade-off:** Slight performance cost vs. preservation of financial document structure integrity.

---

### 2. Context Retriever (`retriever.py`)

**Purpose:** Map financial analysis sections to relevant PDF content using topic-based queries.

**Implementation:**
```python
class ContextRetriever:
    def retrieve_context(self, section_name: str) -> dict:
        """
        Maps section names to predefined financial queries.
        Returns pages and text context for LLM consumption.
        """
        query_map = {
            "executive_summary": "revenue profitability cash flow",
            "financial_metrics": "EBITDA net profit balance sheet",
            "cash_flow_analysis": "cash operating investing financing",
            "risks": "risks borrowings liabilities contingencies",
            "recommendation": "financial position repayment capacity"
        }
        results = vector_store.search(query, top_k=3)
        return {"pages": pages, "context_text": context}
```

**Rationale:**
- **Fixed topic mapping** ensures consistent retrieval behavior across analyses
- **Multi-word queries** improve recall over single keywords
- **Top-K retrieval** (not similarity thresholds) prevents over-fitting to one source
- **Page aggregation** surfaces which pages contributed to each section
---

### 3. Vector Store (`vector_store.py`)

**Purpose:** In-memory searchable index over extracted PDF content.

**Implementation:**
```python
class PageVectorStore:
    def __init__(self, pages: list[dict]):
        """Stores pages; enables full-text search."""
        self.pages = pages  # Keep all metadata (page number, text, tables)
    
    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """
        Simple keyword-in-text matching for now.
        Returns matching pages with their content.
        """
        results = [
            p for p in self.pages 
            if any(word in p['text'] for word in query.split())
        ]
        return results[:top_k]
```

**Current Implementation:**
- **Keyword-based search** – Fast, transparent, auditable
- **Full page content preservation** – No information loss from chunking
- **Metadata attached** – Every result includes page number, original text, tables

**Future Roadmap:**
- Swap keyword search for semantic embeddings (sentence-transformers + FAISS) if multi-year or multi-document analysis needed
- Add table-specific indexing for complex financial tables
- Implement caching for repeated queries

---

### 4. LLM Generator (`credit_memo_generator.py`)

**Purpose:** Synthesize retrieved financial context into structured credit memo using Groq LLM.

**Implementation:**
```python
class CreditMemoGenerator:
    def generate_credit_memo(self) -> dict:
        """
        Generates memo sections sequentially:
        1. Executive Summary (recommendation, key takeaways)
        2. Financial Metrics (extracted figures)
        3. 5Cs Credit Analysis (Character, Capacity, Capital, Collateral, Conditions)
        4. Risk Assessment
        """
        result = {}
        
        # Per-section generation with constrained prompts
        if include_summary:
            result["summary"] = self._generate_executive_summary()
        
        result["financial_metrics"] = self._generate_financial_metrics()
        
        if include_5cs:
            result["credit_analysis_5cs"] = self._generate_5cs()
        
        if include_risks:
            result["risk_assessment"] = self._generate_risks()
        
        return result
```

**Prompting Strategy:**

Each section receives a constrained prompt:

```
You are a banking credit analyst. Analyze the following extracted financial data:

[RETRIEVED CONTEXT FROM PAGES X, Y, Z]

Generate a concise analysis of [section name] following banking standards.
Output ONLY valid JSON with fields: [field_list].
Do not invent data. If information is unavailable, explicitly state: "Not available in provided documents."
```

**Why Constrained Prompts?**
- Prevents hallucination by restricting LLM knowledge to retrieved context
- Explicit JSON schema ensures machine-readable output
- Section-by-section generation allows user to skip irrelevant analyses
- "Information not available" instruction prevents false claims

**Trade-off:** Constrained prompts are less creative than open-ended generation. Acceptable for banking, where accuracy > creativity.

---

### 5. Output Formatting

**JSON Export:**
```json
{
  "metadata": {
    "document_name": "Financial_Statement.pdf",
    "pages_analyzed": 15,
    "overall_confidence": 0.85,
    "model_info": "meta-llama/llama-4-scout-17b"
  },
  "summary": {...},
  "financial_metrics": {...},
  "credit_analysis_5cs": {...},
  "risk_assessment": {...}
}
```

**Word Document (.docx):**
- Formatted memo ready for printing, email, credit committee distribution
- Generated using python-docx for full styling control
- Includes page references and source citations

**Why Dual Output?**
- JSON for system integration (loan management, CRM, workflow automation)
- DOCX for human review and approval (credit committees expect "memo" format)
- Markdown for version control and diffs

---

### 6. User Interfaces

#### Streamlit (Interactive UI)
```
User Flow:
1. Upload PDF
2. System extracts pages (show count, preview)
3. Click "Generate Memo"
4. Memo appears in browser (formatted)
5. Download JSON or DOCX
```

**Rationale:** Rapid prototyping, live preview, no frontend build step required.

#### FastAPI (REST API)
```
POST /upload → Multipart PDF
POST /generate_memo → {"pdf_id": "...", "sections": [...]}
GET /memo/{pdf_id} → JSON response
```

**Rationale:** Headless integration for production workflows; can be called by loan systems.

---

## End-to-End Data Flow

### Phase 1: Ingestion
```
PDF File
  ↓
[PDFProcessor]
  ├─ PyMuPDF: Extract text per page
  ├─ pdfplumber: Extract tables per page
  └─ Output: List of {page_num, text, tables}
  ↓
[PageVectorStore]
  └─ Index: Full-text search on page content
```

**Example Output:**
```
Page 1: "Balance Sheet as of December 31, 2023"
        Assets: Current Assets $1.2M, Fixed Assets $3.5M
        
Page 2: "Cash Flow Statement"
        Operating Activities: $0.8M
        ...
```

### Phase 2: Retrieval
```
Topic Queries (Fixed Mapping)
  ├─ "Executive Summary" → "revenue profitability cash"
  ├─ "Financial Metrics" → "EBITDA net profit"
  ├─ "Risks" → "borrowings liabilities contingencies"
  └─ "Recommendation" → "financial position repayment"

### Phase 3: LLM Analysis
```
[CreditMemoGenerator._generate_risks()]
  ├─ Input:
  │    - Retrieved context (pages 3, 8, 12)
  │    - Prompt: "Analyze risks. Output JSON with: [field_list]. No invented data."
  │
  ├─ Call Groq API (LLaMA-2 or Scout model)
  │
  └─ Output: JSON
       {
         "risks": [
           {
             "category": "Concentration Risk",
             "description": "40% customer concentration mentioned on page 12",
             "page": 12,
             "severity": "High"
           },
           {...}
         ]
       }
```

### Phase 4: Output Generation
```
[JSON Export] → memo.json (structured, machine-readable)
[DOCX Export] → memo.docx (formatted for humans, distribution-ready)
[Metadata]    → processing_time, model_used, pages_analyzed, confidence
```

---

## RAG Design with Source Attribution

### What "RAG" Means Here

**Retrieval-Augmented Generation** in this system:

1. **Retrieval** – Topic-based search of extracted PDF content (not semantic embeddings)
2. **Augmentation** – Retrieved context is passed to LLM as ground truth
3. **Generation** – LLM synthesizes context into structured banking memo


## Why This Architecture Suits Banking

### 1. Auditability
- Every page is numbered from source
- Retrieval logic is transparent (keywords, not embeddings)
- Generated memo includes page citations
- Regulators can reconstruct analysis in minutes

### 2. Reproducibility
- Same PDF + same model = same output (deterministic if temperature=0)
- Metadata stored: model name, pages analyzed, timestamp
- No random vector initialization or hallucination variance

### 3. Compliance-Ready
- No external knowledge injection (closed-world reasoning)
- Explicit "Not available" for missing data (no false confidence)
- Manual analyst review gate before memo approval
- Audit trail: inputs → retrieval → LLM → output

### 4. Integration
- Structured JSON output works with loan management systems (e.g., Black Knight, Ellie Mae)
- DOCX export fits existing workflows (email, credit committee, signing)
- REST API allows headless integration for workflow automation

### 5. Cost-Efficient
- No GPU required (Groq handles inference)
- No embedding model to maintain or fine-tune (for now)
- Per-token pricing vs. infrastructure costs

---

### Evolution Path

**Phase 2:** Add semantic embeddings for multi-document analysis
- Store document vectors in FAISS
- Enable queries like "compare leverage across 3 years"

**Phase 3:** Fine-tune LLM on proprietary credit memo examples
- Improves banking terminology and analysis depth
- Reduce hallucinations with domain-specific training

**Phase 4:** Integrate with live data sources
- Pull industry benchmarks (SEC filings, peer data)
- Real-time covenant monitoring on existing loans

---

## Code Structure

```
mss-backend/
├── api.py                      # FastAPI server
├── app.py                       # Streamlit UI
├── pdf_processor.py             # PDF → Pages
├── vector_store.py              # In-memory index
├── retriever.py                 # Topic-based search
├── credit_memo_generator.py     # LLM synthesis
└── requirements.txt

mss-frontend/
├── src/
│   ├── components/
│   │   ├── FileUpload.jsx
│   │   ├── AnalysisDashboard.jsx
│   │   ├── ReportEditor.jsx
│   │   └── ...
│   └── pages/
└── package.json
```

---

## Conclusion

This architecture prioritizes **trust** and **auditability** over raw capability or speed. Every design choice (keyword search, per-page retrieval, constrained LLM prompts, source citations) serves the goal of making credit memos verifiable and defensible in a banking context.

For a hackathon, the system is **complete and functional**. For production deployment, the roadmap is **clear and scalable** (add embeddings, fine-tune LLM, integrate live data).


