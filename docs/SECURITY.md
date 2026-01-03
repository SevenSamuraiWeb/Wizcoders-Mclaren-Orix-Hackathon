# Security Policy

## Overview

MSS is committed to maintaining a secure platform for financial document analysis. This document outlines our security practices and responsible disclosure process.

## Security Principles

- **Secure by Default:** All features are designed with security in mind
- **Defense in Depth:** Multiple layers of protection
- **Principle of Least Privilege:** Minimal access requirements
- **Auditability:** Complete audit trails for compliance
- **Transparency:** Clear security policies and practices

## Secure Practices

### 1. Secret Management

**✅ DO:**
- Store API keys and credentials in `.env` files (never in code)
- Use environment variables for all sensitive configuration
- Rotate credentials regularly
- Use strong, random secret values

**❌ DON'T:**
- Commit `.env` files to version control
- Hardcode API keys, passwords, or tokens
- Share credentials via email or chat
- Use default or weak credentials

### 2. Authentication & Authorization

- JWT-based authentication with expiration
- Role-based access control (RBAC)
- Session timeout enforcement
- Secure password hashing (bcrypt/argon2)
- MFA support (recommended for production)

### 3. Data Protection

- Encrypted file uploads (TLS/SSL)
- Input validation and sanitization
- SQL injection prevention via parameterized queries
- XSS protection with Content Security Policy
- CSRF tokens for state-changing operations

### 4. API Security

```python
# CORS Configuration (Production)
ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://app.yourdomain.com"
]

# CORS Configuration (Development)
# Use specific domains, NOT ["*"]
```

### 5. Dependency Security

- Regular dependency updates
- Security vulnerability scanning (via GitHub Dependabot)
- Locked dependency versions in production
- License compliance checking

### 6. Infrastructure Security

- Environment-based configuration
- No sensitive data in logs
- Secrets encrypted at rest
- Regular security audits
- Penetration testing (quarterly)

## Configuration Security

### Environment Variables

See `.env.example` for all required variables. Never commit actual `.env` files.

```bash
# Backend .env
OPENAI_API_KEY=sk-...              # Keep secret
ALLOWED_ORIGINS=https://app.example.com
DATABASE_URL=postgresql://user:pass@host/db
JWT_SECRET=your-secret-key-here
DEBUG=false                         # Never True in production
```

### Secure Defaults

```python
# Always use these in production:
CORS_ORIGINS = ["https://yourdomain.com"]  # Specific, not ["*"]
DEBUG = False                              # Never True
ALLOWED_HOSTS = ["yourdomain.com"]         # Specific hosts
HTTPS_ONLY = True                          # Enforce HTTPS
SECURE_COOKIES = True                      # Secure flag
SAMESITE_COOKIES = "Strict"               # CSRF protection
```

## Input Validation

All user inputs are validated:

```python
# Example: File upload validation
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_MIME_TYPES = ["application/pdf"]
ALLOWED_EXTENSIONS = [".pdf"]

# Validate file before processing
assert file.size <= MAX_FILE_SIZE
assert file.mime_type in ALLOWED_MIME_TYPES
assert file.extension in ALLOWED_EXTENSIONS
```

## Logging & Monitoring

**DO log:**
- Authentication attempts (success/failure)
- API access and usage
- File uploads and processing
- System errors and exceptions

**DON'T log:**
- API keys or tokens
- Passwords or credentials
- Sensitive user data (PII)
- Credit card numbers

```python
# ✅ Good logging
logger.info(f"User {user_id} logged in successfully")

# ❌ Bad logging
logger.info(f"User token: {jwt_token}")
logger.info(f"API key: {openai_key}")
```

## Vulnerability Reporting

### Responsible Disclosure

**Found a vulnerability?** Please report it responsibly:

1. **DO NOT** create a public GitHub issue
2. **DO NOT** share details on social media
3. **DO** email: security@example.com
4. Include:
   - Vulnerability description
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if applicable)

### Response Timeline

- **24 hours:** Acknowledgment of receipt
- **7 days:** Initial assessment
- **30 days:** Fix development and testing
- **60 days:** Public disclosure (after coordinated release)

**We will credit researchers for responsible vulnerability reporting.**

## Security Checklist

Before deploying to production:

- [ ] All secrets removed from codebase
- [ ] `.env` files are in `.gitignore`
- [ ] Environment variables properly set
- [ ] CORS origins are specific (not `["*"]`)
- [ ] DEBUG mode is disabled
- [ ] HTTPS is enforced
- [ ] Database connections are encrypted
- [ ] API keys are rotated
- [ ] Logs don't contain sensitive data
- [ ] Dependencies are up-to-date
- [ ] Security headers are configured
- [ ] Input validation is comprehensive
- [ ] Error messages don't leak information
- [ ] Rate limiting is enabled
- [ ] Monitoring and alerting is configured

## Regular Security Updates

We provide security updates for:

- **Critical:** Released immediately
- **High:** Released within 7 days
- **Medium:** Released within 30 days
- **Low:** Released with next major version

## Compliance

This project adheres to:

- ✅ OWASP Top 10 guidelines
- ✅ GitGuardian security standards
- ✅ PCI DSS (where applicable)
- ✅ SOC 2 recommendations
- ✅ GDPR data protection principles

## Security Headers

Production deployments include:

```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

## File Upload Security

- Maximum file size enforced
- File type validation (whitelist-based)
- Virus scanning (recommended)
- Unique filename generation (prevent enumeration)
- Isolated storage location

## Database Security

- Connection encryption (SSL/TLS)
- Strong authentication
- Principle of least privilege
- Regular backups (encrypted)
- Access audit logging

## Third-Party Security

- API keys scoped to minimum permissions
- Regular access audits
- Deprecated APIs removed immediately
- Service provider security reviews

## Questions?

- 📧 Email: security@example.com
- 🔗 Security docs: https://docs.example.com/security
- 📝 Report: [Security Report Form](https://example.com/security-report)

---

**Last Updated:** January 2025
**Next Review:** July 2025
