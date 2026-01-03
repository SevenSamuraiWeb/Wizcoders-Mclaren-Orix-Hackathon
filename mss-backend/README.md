# MSS Backend - Python FastAPI Application

> Production-ready backend API for AI-powered financial document analysis.

## Overview

The MSS backend is built with FastAPI, providing a robust, async-ready REST API for document processing, authentication, and financial analysis.

## Tech Stack

- **Framework:** FastAPI (async Python web framework)
- **Server:** Uvicorn (ASGI)
- **Data Validation:** Pydantic v2
- **Document Processing:** PyMuPDF, PDFPlumber
- **AI/ML:** OpenAI API, Sentence-Transformers, FAISS
- **Authentication:** JWT with python-jose
- **Testing:** pytest with async support
- **Code Quality:** Black, pylint, mypy

## Quick Start

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your values:
# - OPENAI_API_KEY: Your OpenAI API key
# - ALLOWED_ORIGINS: Frontend URL
# - Other settings as needed
```

### Running the Server

```bash
# Development (with auto-reload)
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Production (with 4 workers)
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Access the API at `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`
- OpenAPI Schema: `http://localhost:8000/api/openapi.json`

## Project Structure

```
mss-backend/
├── src/
│   ├── main.py                    # Application entry point
│   ├── core/
│   │   ├── config.py              # Configuration & settings
│   │   ├── logging_config.py      # Logging setup
│   │   ├── security.py            # Security utilities
│   │   └── __init__.py
│   ├── api/
│   │   ├── health.py              # Health check endpoints
│   │   └── v1/
│   │       ├── routes.py          # Route aggregation
│   │       ├── auth.py            # Authentication endpoints
│   │       ├── documents.py       # Document endpoints
│   │       └── __init__.py
│   ├── services/
│   │   ├── document_service.py   # Document processing logic
│   │   └── __init__.py
│   ├── models/
│   │   ├── schemas.py             # Pydantic models
│   │   └── __init__.py
│   └── __init__.py
├── tests/
│   ├── conftest.py                # Pytest configuration
│   ├── test_health.py             # Health check tests
│   ├── test_auth.py               # Authentication tests
│   ├── test_documents.py          # Document processing tests
│   └── fixtures/                  # Test data files
├── config/
│   └── .env.example               # Environment template
├── requirements.txt               # Python dependencies
├── requirements-dev.txt           # Development dependencies
└── README.md                      # This file
```

## API Endpoints

### Health Checks

```
GET /health/status          # API health status
GET /health/live            # Liveness probe
GET /health/ready           # Readiness probe
```

### Authentication

```
POST /api/v1/auth/login     # User login
GET  /api/v1/auth/me        # Get current user
POST /api/v1/auth/refresh   # Refresh access token
```

### Document Processing

```
POST /api/v1/docs/documents/upload      # Upload & analyze document
GET  /api/v1/docs/documents/{doc_id}   # Get analysis results
```

## Development

### Code Quality

**Format code with Black:**
```bash
black src/ tests/
```

**Lint with pylint:**
```bash
pylint src/
```

**Type checking with mypy:**
```bash
mypy src/
```

**Run all quality checks:**
```bash
black src/ tests/ && pylint src/ && mypy src/
```

### Testing

**Run all tests:**
```bash
pytest
```

**Run with coverage:**
```bash
pytest --cov=src tests/
```

**Run specific test file:**
```bash
pytest tests/test_auth.py -v
```

**Run specific test:**
```bash
pytest tests/test_auth.py::test_login -v
```

**Run with specific markers:**
```bash
pytest -m unit        # Run unit tests only
pytest -m integration # Run integration tests
```

### Test Organization

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests (isolated, fast)
│   ├── test_security.py
│   ├── test_models.py
│   └── test_services.py
├── integration/             # Integration tests (slower, real I/O)
│   ├── test_auth_flow.py
│   ├── test_document_upload.py
│   └── test_api_endpoints.py
├── fixtures/                # Test data files
│   ├── sample_credit_memo.pdf
│   └── sample_financial_report.pdf
└── helpers.py              # Test utilities and helpers
```

## Configuration

Configuration is managed through environment variables via `.env` file. See [.env.example](.env.example) for all available options.

### Key Configuration Variables

```
# Server
ENVIRONMENT=development|staging|production
DEBUG=False
HOST=0.0.0.0
PORT=8000
WORKERS=4

# Security
JWT_SECRET=your-secret-key
ALLOWED_ORIGINS=http://localhost:5173

# APIs
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo

# Files
MAX_FILE_SIZE=52428800    # 50MB
ALLOWED_EXTENSIONS=.pdf
UPLOAD_DIR=./uploads
```

### Environment-Specific Defaults

#### Development
- `DEBUG=True`
- `ALLOWED_ORIGINS=["http://localhost:5173", "http://localhost:3000"]`
- `LOG_LEVEL=DEBUG`

#### Production
- `DEBUG=False` (enforced)
- `ALLOWED_ORIGINS=["https://yourdomain.com"]` (specific)
- `LOG_LEVEL=INFO`
- Strong `JWT_SECRET` required
- HTTPS enforced

## Security

- ✅ Environment-based configuration (no hardcoded secrets)
- ✅ JWT token authentication
- ✅ Input validation and sanitization
- ✅ File upload validation
- ✅ CORS protection (configurable)
- ✅ Trusted host middleware
- ✅ Secure error handling

See [SECURITY.md](../SECURITY.md) for detailed security policies.

## Performance

- **Async Processing:** All endpoints are async-ready
- **Structured Logging:** Efficient JSON logging in production
- **Connection Pooling:** Database pooling (when configured)
- **Caching:** Ready for Redis integration
- **Rate Limiting:** Recommended at reverse proxy level

## Troubleshooting

### Common Issues

**ModuleNotFoundError: No module named 'src'**
- Ensure you're running from the `mss-backend` directory
- Check that `src/` directory exists
- Verify virtual environment is activated

**OpenAI API Key Not Found**
- Check `.env` file exists and has `OPENAI_API_KEY` set
- Verify key format is correct: `sk-...`

**CORS Error from Frontend**
- Check `ALLOWED_ORIGINS` in `.env`
- Ensure frontend URL is included
- Restart server after changes

**File Upload Fails**
- Verify `UPLOAD_DIR` directory exists
- Check file size doesn't exceed `MAX_FILE_SIZE`
- Ensure only PDF files are uploaded

## Deployment

See [../docs/SETUP_GUIDE.md](../docs/SETUP_GUIDE.md) for production deployment instructions.

### Quick Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t mss-backend .
docker run -p 8000:8000 --env-file .env mss-backend
```

## Contributing

See [../CONTRIBUTING.md](../CONTRIBUTING.md) for contribution guidelines.

### Pre-commit Setup

```bash
pip install pre-commit
pre-commit install
```

Automatically runs linting and formatting on commit.

## Dependencies

All dependencies are pinned to specific versions for reproducibility.

**Update dependencies:**
```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
```

**Security updates:**
```bash
safety check
pip-audit
```

## Monitoring

### Logging

Logs include:
- Request/response information
- Error stack traces
- Processing metrics
- Security events

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Processing document", extra={"doc_id": "123"})
```

### Health Endpoints

Use health endpoints for container orchestration:
- `/health/live` - Liveness probe (is it alive?)
- `/health/ready` - Readiness probe (is it ready to serve?)
- `/health/status` - Full status check

## Support

- 📖 [API Documentation](http://localhost:8000/api/docs)
- 🐛 [Issue Tracker](https://github.com/username/mss/issues)
- 💬 [Discussions](https://github.com/username/mss/discussions)

---

**Built with FastAPI and ❤️**
