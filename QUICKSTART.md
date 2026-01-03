# Quick Reference Guide

## Project Setup (5 minutes)

### Backend
```bash
cd mss-backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env with your API keys
```

### Frontend
```bash
cd mss-frontend
npm install
cp .env.example .env.local
# Edit .env.local with backend URL
```

## Running the Application

### Start Backend
```bash
cd mss-backend
source venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend
```bash
cd mss-frontend
npm run dev
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## Common Commands

### Backend

| Command | Purpose |
|---------|---------|
| `uvicorn src.main:app --reload` | Start dev server |
| `pytest tests/ -v` | Run all tests |
| `pytest tests/ --cov=src` | Coverage report |
| `black src/ tests/` | Format code |
| `isort src/ tests/` | Sort imports |
| `ruff check src/` | Lint code |
| `mypy src/` | Type checking |
| `bandit -r src/` | Security scan |

### Frontend

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server |
| `npm run build` | Build for production |
| `npm run preview` | Preview build |
| `npm run lint` | Run ESLint |

## Project Structure

```
mss-backend/src/
├── api/v1/              # API routes
├── core/                # Configuration, security
├── models/              # Data schemas
├── services/            # Business logic
└── main.py              # App entry point

mss-frontend/src/
├── pages/               # Page components
├── components/          # Reusable components
├── context/             # State management
├── api.js               # API client
└── utils.js             # Utility functions
```

## Key Files to Know

| File | Purpose |
|------|---------|
| `ARCHITECTURE.md` | System design and architecture |
| `DEVELOPMENT.md` | Development workflow guide |
| `README.md` | Project overview |
| `CONTRIBUTING.md` | How to contribute |
| `SECURITY.md` | Security policies |
| `mss-backend/.env.example` | Backend config template |
| `mss-frontend/.env.example` | Frontend config template |

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_auth_service.py::TestAuthService::test_create_access_token_success

# Run only unit tests
pytest -m unit

# Run with output
pytest -v -s
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, commit with conventional commits
git add .
git commit -m "feat(auth): add token refresh"

# Push and create PR
git push origin feature/my-feature
```

## Environment Variables

### Backend (.env)
```
APP_NAME=MSS Financial Analysis API
ENVIRONMENT=development
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=...
ALLOWED_ORIGINS=http://localhost:5173
```

### Frontend (.env.local)
```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=MSS Financial Analysis
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Get current user

### Documents
- `POST /api/v1/docs/upload` - Upload document
- `GET /api/v1/docs/{id}/analysis` - Get analysis
- `GET /api/v1/docs` - List documents

### Health
- `GET /health` - Health check

## Debugging

### Backend
```python
import ipdb; ipdb.set_trace()  # Breakpoint
```

### Frontend
```javascript
console.log('Debug:', variable)
debugger  // Pause execution
```

## Documentation to Read First

1. **README.md** - Project overview (5 min)
2. **ARCHITECTURE.md** - System design (10 min)
3. **DEVELOPMENT.md** - Development guide (10 min)
4. **Backend README** - Backend specific (10 min)
5. **Frontend README** - Frontend specific (10 min)

## Code Style

### Backend (Python)
- Follow PEP 8
- Use type hints
- Write docstrings
- Format with Black
- Lint with Ruff

### Frontend (JavaScript)
- Use ES6+ syntax
- Follow React best practices
- Add JSDoc comments
- Use functional components
- Lint with ESLint

## Pre-Commit Checklist

Before committing:
- [ ] Code formatted with Black/prettier
- [ ] Imports sorted with isort
- [ ] Linting passes
- [ ] Type checking passes
- [ ] Tests pass
- [ ] No console.log or print in production code
- [ ] Meaningful commit message

## Support & Resources

### Documentation
- API Documentation: http://localhost:8000/api/docs
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- Development Guide: [DEVELOPMENT.md](DEVELOPMENT.md)

### Tools
- Python Docs: https://docs.python.org/3/
- FastAPI: https://fastapi.tiangolo.com/
- React: https://react.dev/
- Vite: https://vitejs.dev/

### Common Issues

**Backend won't start**
- Check .env file exists
- Check port 8000 is available
- Verify Python 3.9+

**Frontend won't load**
- Check backend is running
- Check VITE_API_URL in .env.local
- Clear browser cache (Ctrl+Shift+R)

**Import errors**
- Run `pip install -r requirements-dev.txt`
- Run `npm install`
- Check Python/Node versions

## Performance Tips

### Backend
- Use async/await for I/O
- Implement caching
- Use connection pooling
- Monitor response times

### Frontend
- Lazy load components
- Memoize expensive computations
- Optimize images
- Monitor bundle size

## Security Reminders

- 🔐 Never commit .env files
- 🔑 Never hardcode secrets
- ✅ Validate all inputs
- 🔒 Use HTTPS in production
- 🛡️ Keep dependencies updated
- 📝 Review security logs regularly

## Version Info

- Python: 3.9+ (tested on 3.9, 3.10, 3.11)
- Node: 18+ (recommended 18+)
- FastAPI: 0.109+
- React: 19.2+
- Vite: 6.0+

---

For detailed information, see [DEVELOPMENT.md](DEVELOPMENT.md) or [ARCHITECTURE.md](ARCHITECTURE.md)
