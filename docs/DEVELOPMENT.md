# Development Workflow Guide

This document outlines the recommended workflow for developing and maintaining the MSS Financial Analysis Platform.

## Local Development Setup

### Initial Setup (One-time)

```bash
# Clone the repository
git clone https://github.com/SevenSamuraiWeb/Wizcoders-Mclaren-Orix-Hackathon
cd Wizcoders-Mclaren-Orix-Hackathon

# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Set up backend
cd mss-backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env with your configuration

# Set up frontend (in another terminal)
cd ../mss-frontend
npm install
cp .env.example .env.local
# Edit .env.local with API URL
```

### Daily Development

```bash
# Backend development
cd mss-backend
source venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Frontend development (in another terminal)
cd mss-frontend
npm run dev
```

## Workflow Commands

### Before Committing

```bash
# Format code
cd mss-backend
black src/ tests/
isort src/ tests/

# Lint code
ruff check src/ tests/ --fix
pylint src/

# Type checking
mypy src/

# Run tests
pytest tests/ -v

# Backend: Security scan
bandit -r src/

# Frontend: Lint
cd ../mss-frontend
npm run lint
```

### Running Full Checks Locally

```bash
# All checks script (example)
#!/bin/bash

echo "Running backend checks..."
cd mss-backend
black --check src/ tests/
isort --check src/ tests/
ruff check src/ tests/
mypy src/
pytest tests/ --cov=src
bandit -r src/

echo "Running frontend checks..."
cd ../mss-frontend
npm run lint
npm run build

echo "All checks passed!"
```

## Git Workflow

### Branch Naming

```
feature/user-authentication     # New features
bugfix/login-validation-error   # Bug fixes
docs/api-documentation         # Documentation
refactor/module-structure       # Code refactoring
test/increase-coverage          # Test additions
chore/dependency-update         # Dependency updates
```

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>

# Example:
feat(auth): implement JWT token verification

- Add JWT verification in auth middleware
- Add token expiration handling
- Add unit tests for auth flow

Closes #42
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style (formatting, missing semicolons)
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `chore`: Build process, dependencies

### Pull Request Process

1. Create feature branch from `develop`
2. Make commits with descriptive messages
3. Push to fork and create PR to main repo
4. Wait for CI/CD to pass
5. Request review from team members
6. Address review feedback
7. Merge when approved

## Testing Strategy

### Unit Tests

```bash
# Run only unit tests
pytest -m unit

# Run with coverage
pytest -m unit --cov=src --cov-report=html

# Run specific test file
pytest tests/test_auth_service.py -v
```

### Integration Tests

```bash
# Run integration tests
pytest -m integration

# Run all tests
pytest tests/
```

### Test Coverage Goals

- **Overall**: 70%+ coverage
- **Services**: 85%+ coverage
- **API Routes**: 80%+ coverage
- **Utils**: 60%+ coverage

### Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=src --cov-report=html

# Open report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov\index.html  # Windows
```

## Code Review Checklist

### For Backend PRs

- [ ] Code follows PEP 8 style guide
- [ ] All functions have type hints
- [ ] Docstrings for all public functions
- [ ] No hardcoded secrets
- [ ] Tests added for new functionality
- [ ] Tests pass locally
- [ ] No new linting errors
- [ ] No console.log or print statements
- [ ] Database queries are efficient
- [ ] Error handling is comprehensive

### For Frontend PRs

- [ ] Code follows React best practices
- [ ] Components are focused and reusable
- [ ] No console.log in production code
- [ ] No hardcoded API URLs
- [ ] Responsive design verified
- [ ] ESLint passes
- [ ] Build completes successfully
- [ ] No large dependencies added without justification

## Debugging

### Backend Debugging

```python
# Add breakpoints
import pdb; pdb.set_trace()

# Or use ipdb (better)
import ipdb; ipdb.set_trace()

# Or use VS Code debugger with launch config
```

### Frontend Debugging

```javascript
// React DevTools browser extension
// Open DevTools: F12
// Source tab for breakpoints
// Console tab for logs
// Network tab for API calls

// Add debugging
console.log('Debug info:', variable)
debugger  // Pause execution
```

### API Testing

```bash
# Using curl
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'

# Using httpie (better)
http POST localhost:8000/api/v1/auth/login \
  email=test@example.com password=password123

# Using Postman
# Import collection from docs/postman-collection.json
```

## Deployment

### Staging Deployment

```bash
# Create staging branch
git checkout -b release/v0.2.0

# Run full test suite
pytest tests/ --cov=src

# Update version numbers
# - mss-backend/src/core/config.py
# - mss-frontend/package.json

# Commit changes
git add -A
git commit -m "chore(release): bump version to 0.2.0"

# Push to staging
git push origin release/v0.2.0

# Create pull request to staging branch
```

### Production Deployment

```bash
# Merge staging to main
git checkout main
git merge release/v0.2.0

# Create git tag
git tag -a v0.2.0 -m "Release version 0.2.0"

# Push to production
git push origin main --tags

# Deploy (CI/CD automatically handles this)
```

## Monitoring & Logging

### View Logs

```bash
# Development
tail -f logs/app.log  # macOS/Linux
Get-Content logs\app.log -Tail 10 -Wait  # Windows

# Check specific error
grep "ERROR" logs/app.log
```

### Health Check

```bash
# Local
curl http://localhost:8000/health

# Staging/Production
curl https://api.yourdomain.com/health
```

## Common Issues & Solutions

### Virtual Environment Issues

```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

### Dependency Conflicts

```bash
# Update all dependencies
pip install --upgrade -r requirements.txt

# Check for conflicts
pip check

# Security audit
pip-audit
```

### Node Modules Issues

```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

## Performance Tips

### Backend

- Use async/await for I/O operations
- Implement caching for expensive operations
- Use connection pooling for databases
- Monitor API response times

### Frontend

- Lazy load components with React.lazy()
- Memoize expensive computations
- Optimize images and assets
- Use production builds for testing

## Documentation Maintenance

When making code changes:
1. Update relevant docstrings
2. Update ARCHITECTURE.md if structure changes
3. Update README.md for user-facing changes
4. Add comments for complex logic
5. Keep CHANGELOG.md updated

## Release Process

1. Create release branch from develop
2. Update version numbers
3. Update CHANGELOG.md
4. Run full test suite
5. Create PR to main
6. After merge, create git tag
7. Update GitHub release notes
8. Deploy to production
