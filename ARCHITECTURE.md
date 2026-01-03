# Architecture Documentation

## System Overview

This document describes the architecture of the MSS Financial Analysis Platform, including system design, component interactions, and deployment patterns.

```
┌─────────────────────────────────────────────────────────────┐
│                  CLIENT LAYER (React/Vite)                │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Pages:  Login  │  Dashboard  │  Analysis        │  │
│  │  Components: FileUpload, PDFViewer, Analysis     │  │
│  │  State: AuthContext, LocalStorage                │  │
│  └─────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTPS + JWT
┌────────────────────────────▼────────────────────────────────┐
│                 API GATEWAY LAYER (FastAPI)               │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Middleware: CORS, TrustedHost, Logging            │  │
│  │  Routes: /api/v1/auth, /api/v1/docs, /health      │  │
│  │  Error Handling: Centralized exception handlers    │  │
│  └─────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│               BUSINESS LOGIC LAYER (Services)             │
│  ┌──────────────────┬──────────────────┬────────────────┐ │
│  │ AuthService      │ DocumentService  │ AnalysisService│ │
│  │ - Login/Token    │ - Extract text   │ - Generate     │ │
│  │ - Verification   │ - Parse PDF/DOCX │ - Summarize    │ │
│  │ - User mgmt      │ - Validate       │ - LLM calls    │ │
│  └──────────────────┴──────────────────┴────────────────┘ │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│              ML/AI LAYER (Intelligence Engine)            │
│  ┌──────────────────┬──────────────────┬────────────────┐ │
│  │ Document Parser  │ Embeddings       │ LLM Integration│ │
│  │ - PyMuPDF        │ - Sentence-Trans │ - OpenAI API   │ │
│  │ - PDFPlumber     │ - FAISS Vector   │ - Prompt Eng.  │ │
│  │ - python-docx    │ - Similarity     │ - Few-shot     │ │
│  └──────────────────┴──────────────────┴────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Frontend Structure (`mss-frontend/src`)

```
src/
├── pages/
│   ├── Login.jsx          # Authentication entry point
│   └── Dashboard.jsx      # Main application dashboard
├── components/
│   ├── Layout.jsx         # Main layout wrapper
│   ├── Header.jsx         # Navigation header
│   ├── Sidebar.jsx        # Navigation sidebar
│   ├── FileUpload.jsx     # Document upload handler
│   ├── PDFViewer.jsx      # PDF visualization
│   ├── AnalysisDashboard.jsx  # Analysis display
│   └── ProtectedRoute.jsx # Auth guard wrapper
├── context/
│   └── AuthContext.jsx    # Global auth state
├── utils.js               # Helper functions
└── assets/                # Static resources
```

**Key Patterns:**
- Context API for global state management
- Functional components with React hooks
- Protected routes for authenticated pages
- Composition-based component design

### Backend Structure (`mss-backend/src`)

```
src/
├── api/
│   ├── health.py          # Health check endpoints
│   └── v1/
│       ├── auth.py        # Authentication routes
│       ├── documents.py   # Document endpoints
│       └── routes.py      # Route aggregation
├── core/
│   ├── config.py          # Configuration management
│   ├── security.py        # Security utilities
│   ├── logging_config.py  # Logging setup
│   └── exceptions.py      # Custom exceptions
├── models/
│   ├── schemas.py         # Request/response schemas
│   └── domain.py          # Domain models
├── services/
│   ├── document_service.py    # Document processing
│   ├── analysis_service.py    # AI-powered analysis
│   └── auth_service.py        # Authentication logic
└── main.py                # Application factory
```

**Key Patterns:**
- Layered architecture (API → Services → ML)
- Configuration-driven behavior
- Comprehensive error handling
- Async/await for I/O operations

## Data Flow

### Document Upload & Analysis Flow

```
1. Frontend: User uploads file
   ↓ (FormData with auth token)
2. API: POST /api/v1/docs/upload
   ↓ (Validation, file storage)
3. DocumentService: Parse & extract
   ↓ (PyMuPDF/PDFPlumber)
4. AnalysisService: Generate embeddings
   ↓ (Sentence-Transformers)
5. LLM Integration: Get analysis
   ↓ (OpenAI API with prompt)
6. Frontend: Display results
```

### Authentication Flow

```
1. Frontend: User submits credentials
   ↓ (POST /api/v1/auth/login)
2. AuthService: Validate & generate JWT
   ↓ (Create access token)
3. Frontend: Store token + auth state
   ↓ (localStorage + AuthContext)
4. Protected Routes: Verify token
   ↓ (Check expiration & validity)
5. Requests: Include JWT in headers
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 19, Vite, Tailwind CSS | Modern, fast web UI |
| **Backend** | FastAPI, Uvicorn | Async REST API |
| **Validation** | Pydantic, pydantic-settings | Data validation |
| **Documents** | PyMuPDF, PDFPlumber, python-docx | File parsing |
| **AI/ML** | OpenAI, Sentence-Transformers, FAISS | Intelligent analysis |
| **Auth** | PyJWT, bcrypt | Secure authentication |
| **Testing** | pytest, pytest-asyncio | Automated testing |
| **Logging** | Python logging | Observability |

## Deployment Architecture

### Development Environment
- Backend: `uvicorn src.main:app --reload` (local dev server)
- Frontend: `npm run dev` (Vite dev server)
- Environment: `.env` with development keys

### Staging Environment
- Backend: Docker container on staging cluster
- Frontend: Built SPA deployed to CDN
- Environment: Encrypted `.env` on secure server

### Production Environment
- Backend: Kubernetes pod with multiple replicas
- Frontend: SPA on CDN with edge caching
- Environment: Secrets managed by cloud provider
- Monitoring: Centralized logging and alerting

## Security Architecture

### Authentication & Authorization

- **JWT Tokens:** Stateless authentication with expiration
- **CORS:** Restricted to known origins only
- **TrustedHost:** Validate Host header
- **Input Validation:** Pydantic schemas
- **HTTPS:** Required in production

### Data Protection

- **File Uploads:** Temporary storage with cleanup
- **API Keys:** Environment variables only
- **Database:** (Future) Encrypted credentials
- **Audit Logging:** All auth events logged

## Scaling Considerations

### Horizontal Scaling
- Stateless API design
- Load balancer for multiple backend instances
- CDN for frontend assets
- Message queue for async tasks (future)

### Caching Strategy
- Browser caching for static assets
- API response caching for expensive operations
- Embedding cache to avoid recomputation

### Performance Optimization
- Lazy loading of components
- Async document processing
- Vector search for similarity matching
- Request/response compression

## Monitoring & Observability

### Logging
- Structured logging with JSON format
- Configurable log levels
- Request/response logging
- Error tracking and alerting

### Metrics
- API response times
- Document processing duration
- API error rates
- Token validation failures

### Health Checks
- `/health` endpoint for readiness
- Dependency health status
- Error rate monitoring

## Error Handling Strategy

### API Errors
- Standardized JSON error responses
- HTTP status codes (4xx client, 5xx server)
- Detailed error messages (development) vs. generic (production)
- Error tracking for debugging

### Graceful Degradation
- Fallback responses for AI failures
- Partial results if some processing fails
- User-friendly error messages

## Future Architecture Improvements

1. **Database Layer:** Add PostgreSQL for user data persistence
2. **Caching Layer:** Redis for session and response caching
3. **Message Queue:** Celery for async document processing
4. **Observability:** Prometheus + Grafana for metrics
5. **API Gateway:** Kong or similar for rate limiting
6. **Microservices:** Separate document processing microservice
7. **GraphQL:** Optional GraphQL API for frontend flexibility
