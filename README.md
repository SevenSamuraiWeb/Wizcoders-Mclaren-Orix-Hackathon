# MSS Financial Analysis Platform

> Enterprise-grade AI-powered financial document analysis system for intelligent credit memo and financial report processing.

![Python](https://img.shields.io/badge/Python-3.9+-3776ab?style=flat&logo=python)
![React](https://img.shields.io/badge/React-19.2+-61dafb?style=flat&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?style=flat&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green)
![Security](https://img.shields.io/badge/Security-GitGuardian%20Compliant-blue)

## Problem Statement

Financial professionals spend significant time manually extracting and analyzing key metrics from credit memos, financial reports, and annual statements. This process is error-prone, time-consuming, and limits the depth of analysis possible in real-time decision-making.

**Solution:** MSS delivers AI-powered document intelligence that instantly extracts financial metrics, identifies risk factors, and provides comprehensive analysis—transforming hours of manual work into seconds of insight.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React/Vite)               │
│  • Secure file upload with drag-and-drop UI           │
│  • PDF viewer with document inspection                │
│  • Real-time analysis dashboard                       │
│  • Authentication & authorization layer               │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS + JWT Auth
┌────────────────────▼────────────────────────────────────┐
│                   Backend (FastAPI)                     │
│  • RESTful API with comprehensive validation           │
│  • Document processing pipeline                       │
│  • AI-powered financial intelligence                  │
│  • CORS-protected, audit-ready                        │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Core ML/AI Services                        │
│  • PyMuPDF & PDFPlumber for document extraction       │
│  • Sentence-Transformers for semantic understanding   │
│  • FAISS for intelligent similarity search            │
│  • OpenAI GPT integration for analysis                │
└─────────────────────────────────────────────────────────┘
```

## Tech Stack

**Backend:**
- **Framework:** FastAPI (async Python web framework)
- **Document Processing:** PyMuPDF, PDFPlumber, python-docx
- **AI/ML:** Sentence-Transformers, FAISS, OpenAI API
- **Server:** Uvicorn (ASGI server)
- **Testing:** pytest, pytest-asyncio

**Frontend:**
- **Framework:** React 19 with Vite
- **UI Components:** Lucide React (icon system)
- **Styling:** Tailwind CSS with modern utilities
- **PDF Viewing:** react-pdf
- **Routing:** React Router v7
- **State Management:** React Context API
- **File Handling:** react-dropzone

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### Backend Setup

```bash
# Clone repository
git clone <repository-url>
cd Wizcoders-Mclaren-Orix-Hackathon

# Set up Python environment
cd mss-backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run development server
python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Install dependencies
cd ../mss-frontend
npm install

# Configure environment
cp .env.example .env

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
.
├── mss-backend/                    # Python FastAPI backend
│   ├── src/
│   │   ├── main.py                # Application entry point
│   │   ├── core/                  # Core utilities & config
│   │   ├── api/                   # API routes & endpoints
│   │   ├── services/              # Business logic layer
│   │   └── models/                # Data models & schemas
│   ├── tests/                     # Unit & integration tests
│   ├── config/                    # Environment & config files
│   ├── requirements.txt           # Python dependencies
│   └── README.md                  # Backend documentation
│
├── mss-frontend/                  # React frontend
│   ├── src/
│   │   ├── components/            # Reusable React components
│   │   ├── pages/                 # Page-level components
│   │   ├── context/               # React Context providers
│   │   ├── hooks/                 # Custom React hooks
│   │   ├── services/              # API & external service calls
│   │   ├── utils/                 # Utility functions
│   │   ├── assets/                # Images, fonts, static files
│   │   ├── App.jsx                # Root component
│   │   └── main.jsx               # Entry point
│   ├── tests/                     # Frontend tests
│   ├── public/                    # Static files
│   ├── package.json               # Node dependencies
│   └── README.md                  # Frontend documentation
│
├── docs/                          # Project documentation
│   ├── ARCHITECTURE.md            # Detailed architecture
│   ├── API.md                     # API documentation
│   └── SETUP_GUIDE.md             # Development setup guide
│
├── scripts/                       # Automation & tooling
│   ├── setup.sh                   # One-command setup
│   └── validate.sh                # Code quality checks
│
├── config/                        # Shared configuration
│   ├── docker-compose.yml         # Local development stack
│   └── nginx.conf                 # Production reverse proxy
│
├── .github/workflows/             # CI/CD pipelines
│   ├── test.yml                   # Test automation
│   └── deploy.yml                 # Production deployment
│
├── SECURITY.md                    # Security policy
├── CONTRIBUTING.md                # Contributing guidelines
├── CHANGELOG.md                   # Version history
└── README.md                      # This file
```

## Core Features

- ✅ **Intelligent Document Analysis** - AI-powered extraction of financial metrics and risk factors
- ✅ **Secure File Upload** - Encrypted file handling with validation
- ✅ **Real-time Processing** - Async document processing with progress tracking
- ✅ **Authentication** - JWT-based user authentication and role-based access control
- ✅ **Responsive UI** - Modern, accessible design for all devices
- ✅ **RESTful API** - Comprehensive API with comprehensive input validation
- ✅ **Audit Logging** - Complete audit trail for compliance

## API Documentation

See [API.md](docs/API.md) for comprehensive API endpoint documentation.

### Example Request

```bash
curl -X POST http://localhost:8000/api/v1/documents/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@credit_memo.pdf"
```

## Development Guide

### Running Tests

**Backend:**
```bash
cd mss-backend
pytest --cov=src tests/
```

**Frontend:**
```bash
cd mss-frontend
npm test
```

### Code Quality

**Linting & Formatting:**
```bash
# Backend
black src/ tests/
pylint src/
mypy src/

# Frontend
npm run lint
```

**Pre-commit hooks:**
See [CONTRIBUTING.md](CONTRIBUTING.md) for setup instructions.

## Security

This project implements security best practices aligned with GitGuardian standards:

- ✅ No hardcoded secrets or credentials
- ✅ Environment-based configuration via `.env` files
- ✅ Input validation and sanitization
- ✅ CORS properly configured for production
- ✅ HTTPS enforcement in production
- ✅ Dependency scanning via renovate
- ✅ Regular security audits

**Security Issues:** See [SECURITY.md](SECURITY.md) for responsible disclosure.

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Code style and standards
- Pull request process
- Testing requirements
- Commit message conventions

## Deployment

See [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for production deployment instructions including:
- Docker containerization
- Kubernetes deployment
- AWS/Azure cloud deployment
- GitHub Actions CI/CD

## Performance & Scaling

- Async request handling for high throughput
- FAISS vector DB for efficient similarity search
- Caching strategies for frequently accessed data
- Horizontal scaling with load balancing
- Database connection pooling

## Troubleshooting

**Issue:** `CORS error when uploading files`
- Solution: Verify backend is running on correct port and check CORS configuration in `.env`

**Issue:** `PDF parsing errors`
- Solution: Ensure file is a valid PDF; see logs for specific format issues

**Issue:** `API authentication fails`
- Solution: Check JWT token expiration; re-login if necessary

For more help, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) or open an issue.

## Roadmap

- [ ] Advanced financial ratio analysis
- [ ] Multi-document comparison
- [ ] Custom report generation
- [ ] Webhooks for event-driven workflows
- [ ] GraphQL API option
- [ ] Mobile app support

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Citation

If you use MSS in your research or projects, please cite:

```bibtex
@software{mss_hackathon,
  title={MSS Financial Analysis Platform},
  author={Team Name},
  year={2025},
  url={https://github.com/username/mss}
}
```

## Support

- 📧 Email: support@example.com
- 💬 Discord: [Community Channel](https://discord.gg/example)
- 📖 Docs: https://mss-docs.example.com
- 🐛 Issues: https://github.com/username/mss/issues

---

**Built with ❤️ by the MSS Team**
