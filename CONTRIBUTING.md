# Contributing to MSS Financial Analysis Platform

Thank you for your interest in contributing! This document provides guidelines for contributing to the MSS project.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all. Please read and adhere to our Code of Conduct.

**Our Pledge:**
- Be respectful and inclusive
- Welcome newcomers and help them get oriented
- Focus on ideas, not persons
- Report inappropriate behavior to the maintainers

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git
- VS Code or preferred IDE
- Docker (optional, for containerized development)

### Local Development Setup

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/mss.git
cd mss

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/mss.git

# 4. Create a feature branch
git checkout -b feature/your-feature-name

# 5. Set up backend
cd mss-backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 6. Set up frontend
cd ../mss-frontend
npm install

# 7. Configure environment
cd ../mss-backend
cp .env.example .env
# Edit .env with your local values
```

### Development Workflow

```bash
# 1. Keep your fork updated
git fetch upstream
git rebase upstream/main

# 2. Make changes
# - Frontend: mss-frontend/src/
# - Backend: mss-backend/src/

# 3. Test your changes
cd mss-backend && pytest
cd ../mss-frontend && npm test

# 4. Lint and format
cd mss-backend && black src/ && pylint src/
cd ../mss-frontend && npm run lint

# 5. Commit with clear messages
git commit -m "feat: add document comparison feature"

# 6. Push to your fork
git push origin feature/your-feature-name

# 7. Create a Pull Request
```

## Coding Standards

### Python (Backend)

**Style Guide:** PEP 8

```python
# Format with Black
black src/ tests/

# Type hints required
def process_document(file_path: str, model_name: str) -> dict:
    """Process PDF document and extract metrics.
    
    Args:
        file_path: Path to PDF file
        model_name: Name of ML model to use
        
    Returns:
        Dictionary with extracted metrics
    """
    # Implementation
    pass

# Docstrings: Google style
# Imports: isort formatted
```

**Tools:**
- **Formatter:** `black` (100 character line length)
- **Linter:** `pylint` (8.5+ score target)
- **Type Checker:** `mypy`
- **Testing:** `pytest`

**Setup tools:**
```bash
pip install black pylint mypy pytest pytest-cov pytest-asyncio
```

### JavaScript/React (Frontend)

**Style Guide:** Modern ES6+ with React best practices

```jsx
// Use functional components with hooks
export function FileUpload({ onFileUpload }) {
  const [files, setFiles] = useState(null);
  
  // Proper component documentation
  useEffect(() => {
    // Effect implementation
  }, []);
  
  return <div>{/* JSX */}</div>;
}

// Export statement
export default FileUpload;
```

**Tools:**
- **Linter:** ESLint (included in project)
- **Formatter:** Prettier (or use Tailwind's formatting)
- **Testing:** Vitest or Jest
- **Type Checking:** JSDoc comments (recommended)

**Commands:**
```bash
npm run lint              # Check for linting issues
npm run lint:fix         # Auto-fix linting issues
npm run format           # Format code with Prettier
npm run type-check       # Check types with JSDoc
```

## Commit Message Guidelines

Follow semantic commit messages:

```
<type>(<scope>): <subject>
<blank line>
<body>
<blank line>
<footer>
```

### Types

- **feat:** New feature
- **fix:** Bug fix
- **docs:** Documentation changes
- **style:** Code style changes (formatting, semicolons, etc.)
- **refactor:** Code refactoring without behavior change
- **perf:** Performance improvements
- **test:** Adding or updating tests
- **chore:** Build, dependencies, tooling
- **security:** Security improvements

### Examples

```
feat(auth): implement JWT token refresh mechanism

- Add refresh token endpoint
- Store refresh tokens in Redis
- Implement token rotation strategy
- Add tests for token refresh flow

Fixes #123
```

```
fix(pdf-parser): handle corrupted PDF files gracefully

Validates PDF structure before processing and returns
meaningful error message when file is corrupted.

Fixes #456
```

## Pull Request Process

### Before Submitting

1. **Rebase on main:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run tests:**
   ```bash
   # Backend
   cd mss-backend
   pytest --cov=src

   # Frontend
   cd ../mss-frontend
   npm test
   ```

3. **Lint and format:**
   ```bash
   # Backend
   black src/
   pylint src/
   mypy src/

   # Frontend
   npm run lint:fix
   ```

4. **Update docs** if behavior changes

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #(issue number)

## Testing
Describe testing performed:
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests pass locally
```

## Testing Guidelines

### Backend Testing

```python
# Location: mss-backend/tests/
# File naming: test_<module>.py

import pytest
from src.services.document_processor import extract_metrics

def test_extract_metrics_from_valid_pdf():
    """Test metric extraction from valid PDF."""
    # Arrange
    test_file = "tests/fixtures/sample_credit_memo.pdf"
    
    # Act
    result = extract_metrics(test_file)
    
    # Assert
    assert result is not None
    assert "total_debt" in result
    assert result["total_debt"] > 0

@pytest.mark.asyncio
async def test_async_document_processing():
    """Test async document processing."""
    # Implementation
    pass

def test_invalid_file_raises_error():
    """Test error handling for invalid files."""
    with pytest.raises(ValueError):
        extract_metrics("invalid.txt")
```

**Run tests:**
```bash
pytest                          # Run all tests
pytest tests/test_auth.py       # Run specific file
pytest -k "test_extract"        # Run specific test
pytest --cov=src               # With coverage report
pytest -v                       # Verbose output
```

### Frontend Testing

```javascript
// Location: mss-frontend/tests/
// File naming: <Component>.test.jsx

import { render, screen, fireEvent } from '@testing-library/react';
import FileUpload from '../components/FileUpload';

describe('FileUpload Component', () => {
  it('renders upload button', () => {
    render(<FileUpload onFileUpload={() => {}} />);
    const button = screen.getByText(/Browse Files/i);
    expect(button).toBeInTheDocument();
  });

  it('calls onFileUpload when file is dropped', () => {
    const mockHandler = jest.fn();
    const { container } = render(<FileUpload onFileUpload={mockHandler} />);
    
    // Simulate file drop
    // Assert handler was called
  });
});
```

**Run tests:**
```bash
npm test                        # Run all tests
npm test -- FileUpload         # Run specific file
npm test -- --coverage         # With coverage
```

## Documentation

### Code Comments

Use clear, concise comments:

```python
# ✅ Good: Explains why, not what
# Cache results to avoid repeated API calls
cache[key] = expensive_operation()

# ❌ Bad: States the obvious
# Increment counter
counter += 1

# ✅ Good: Complex logic explanation
# Use FAISS for fast similarity search on embeddings
# because it's 100x faster than brute-force distance calculation
similarity_scores = faiss_index.search(query_embedding, k=5)
```

### Documentation Files

- **README.md:** Project overview and quick start
- **ARCHITECTURE.md:** Design decisions and system architecture
- **API.md:** API endpoint documentation
- **CONTRIBUTING.md:** Contributing guidelines (this file)
- **SECURITY.md:** Security policies
- **CHANGELOG.md:** Version history

### API Documentation

Use docstrings for all endpoints:

```python
@router.post("/documents/analyze")
async def analyze_document(file: UploadFile) -> dict:
    """
    Analyze a financial document.
    
    Args:
        file: PDF file to analyze (max 50MB)
        
    Returns:
        Analysis results with extracted metrics
        
    Raises:
        HTTPException 400: Invalid file format
        HTTPException 413: File too large
        HTTPException 500: Processing error
        
    Example:
        POST /api/v1/documents/analyze
        Content-Type: multipart/form-data
        
        Response:
        {
            "total_debt": 1000000,
            "equity": 500000,
            "risk_factors": ["..."]
        }
    """
    # Implementation
    pass
```

## Issue Reporting

### Bug Reports

Include:
- Environment (OS, Python version, etc.)
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots or error logs
- Attempted solutions

### Feature Requests

Include:
- Problem statement
- Proposed solution
- Alternatives considered
- Use cases

## Release Process

We follow semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR:** Incompatible changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

Releases are coordinated by maintainers.

## Project Structure

```
mss/
├── mss-backend/          # Python FastAPI backend
├── mss-frontend/         # React Vite frontend
├── docs/                 # Documentation
├── scripts/              # Development scripts
├── config/               # Configuration
└── .github/workflows/    # CI/CD
```

## Communication

- **Issues:** For bugs and feature requests
- **Discussions:** For questions and ideas
- **Email:** security@example.com for security issues

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

## Additional Resources

- [GitHub Issues](https://github.com/username/mss/issues)
- [Project Discussions](https://github.com/username/mss/discussions)
- [Security Policy](SECURITY.md)
- [Changelog](CHANGELOG.md)

---

**Thank you for contributing!** 🚀

Questions? Open a discussion or reach out to the maintainers.
