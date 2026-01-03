# Legacy Code Archive

This folder contains legacy code from the original implementation, preserved for reference during the migration to the new modular architecture.

## Files

### Applications
- **app.py** - Streamlit-based UI application (original prototype)
- **api.py** - Original FastAPI implementation (pre-refactoring)

### Core Modules (Old Structure)
- **credit_memo_generator.py** - Credit memo generation logic using Groq LLM
- **retriever.py** - Context retrieval using vector search
- **vector_store.py** - FAISS-based vector storage and similarity search
- **pdf_processor.py** - PDF text extraction (if exists)

### Test Data & Config
- **Financial_Statement.pdf** - Sample financial statement for testing
- **quarterly_report.pdf** - Sample quarterly report for testing
- **setup.txt** - Original setup instructions

## Migration Status

The functionality from these files is being migrated to the new modular structure:

| Legacy Module | New Location | Status |
|--------------|--------------|--------|
| `credit_memo_generator.py` | `src/services/analysis_service.py` | ⚠️ TODO |
| `retriever.py` | `src/services/analysis_service.py` | ⚠️ TODO |
| `vector_store.py` | `src/services/analysis_service.py` | ⚠️ TODO |
| `pdf_processor.py` | `src/services/document_service.py` | ⚠️ TODO |
| `api.py` routes | `src/api/v1/` | ✅ Migrated |

## Important Notes

1. **DO NOT USE** these files directly in the new codebase
2. **Reference only** - Use as a guide for implementing the new services
3. **Dependencies**: These files use old import paths and won't work with the new structure
4. **Testing**: Sample PDF files should be moved to `tests/fixtures/` when writing tests

## Next Steps

1. Implement PDF processing in `src/services/document_service.py`:
   - Extract text from PDF using PyMuPDF/PDFPlumber
   - Parse financial statements
   - Extract structured data

2. Implement AI analysis in `src/services/analysis_service.py`:
   - Vector embedding generation (Sentence-Transformers)
   - FAISS similarity search
   - LLM-powered analysis (OpenAI/Groq)
   - Credit memo generation

3. Add comprehensive tests in `tests/`:
   - Use sample PDFs from `tests/fixtures/`
   - Test each service independently
   - Integration tests for full workflow

## Deletion Timeline

These files will be removed once:
- [ ] All functionality is migrated to new services
- [ ] Comprehensive tests are written and passing
- [ ] Documentation is complete
- [ ] Team confirms no dependencies remain

**Estimated Timeline**: After successful deployment of refactored version

---

*For questions about migration, see [../docs/DEVELOPMENT.md](../../docs/DEVELOPMENT.md)*
