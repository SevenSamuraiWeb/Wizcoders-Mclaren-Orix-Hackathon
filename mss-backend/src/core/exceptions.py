"""
Custom Exception Classes

Defines domain-specific exceptions for cleaner error handling
and better error propagation throughout the application.
"""


class MSSSException(Exception):
    """Base exception for all MSS application errors."""

    def __init__(self, message: str, error_code: str = None, status_code: int = 500):
        """
        Initialize the exception.

        Args:
            message: Human-readable error message
            error_code: Machine-readable error code
            status_code: HTTP status code to return
        """
        self.message = message
        self.error_code = error_code or "INTERNAL_ERROR"
        self.status_code = status_code
        super().__init__(self.message)


# ============================================================================
# Authentication Exceptions
# ============================================================================


class AuthenticationError(MSSSException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_FAILED",
            status_code=401
        )


class InvalidTokenError(AuthenticationError):
    """Raised when JWT token is invalid or expired."""

    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)
        self.error_code = "INVALID_TOKEN"


class UnauthorizedError(MSSSException):
    """Raised when user lacks required permissions."""

    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            message=message,
            error_code="UNAUTHORIZED",
            status_code=403
        )


# ============================================================================
# Document Processing Exceptions
# ============================================================================


class DocumentProcessingError(MSSSException):
    """Raised when document processing fails."""

    def __init__(self, message: str = "Document processing failed"):
        super().__init__(
            message=message,
            error_code="DOCUMENT_PROCESSING_ERROR",
            status_code=400
        )


class UnsupportedFileTypeError(DocumentProcessingError):
    """Raised when file type is not supported."""

    def __init__(self, file_type: str):
        message = f"Unsupported file type: {file_type}"
        super().__init__(message)
        self.error_code = "UNSUPPORTED_FILE_TYPE"


class FileSizeExceededError(DocumentProcessingError):
    """Raised when file size exceeds maximum allowed."""

    def __init__(self, max_size_mb: int):
        message = f"File size exceeds maximum of {max_size_mb}MB"
        super().__init__(message)
        self.error_code = "FILE_SIZE_EXCEEDED"


class FileNotFoundError(DocumentProcessingError):
    """Raised when file is not found."""

    def __init__(self, filename: str):
        message = f"File not found: {filename}"
        super().__init__(message)
        self.error_code = "FILE_NOT_FOUND"


# ============================================================================
# AI & Analysis Exceptions
# ============================================================================


class AnalysisError(MSSSException):
    """Raised when analysis operations fail."""

    def __init__(self, message: str = "Analysis failed"):
        super().__init__(
            message=message,
            error_code="ANALYSIS_ERROR",
            status_code=500
        )


class LLMError(AnalysisError):
    """Raised when LLM (Large Language Model) API calls fail."""

    def __init__(self, message: str = "LLM service unavailable"):
        super().__init__(message)
        self.error_code = "LLM_ERROR"


class EmbeddingError(AnalysisError):
    """Raised when embedding generation fails."""

    def __init__(self, message: str = "Embedding generation failed"):
        super().__init__(message)
        self.error_code = "EMBEDDING_ERROR"


# ============================================================================
# Validation Exceptions
# ============================================================================


class ValidationError(MSSSException):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: str = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422
        )
        self.field = field


class InvalidCredentialsError(ValidationError):
    """Raised when credentials are invalid."""

    def __init__(self):
        super().__init__(
            message="Invalid email or password",
            field="credentials"
        )
        self.error_code = "INVALID_CREDENTIALS"


# ============================================================================
# Configuration Exceptions
# ============================================================================


class ConfigurationError(MSSSException):
    """Raised when configuration is invalid or missing."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="CONFIGURATION_ERROR",
            status_code=500
        )


class MissingEnvironmentVariableError(ConfigurationError):
    """Raised when required environment variable is missing."""

    def __init__(self, var_name: str):
        message = f"Missing required environment variable: {var_name}"
        super().__init__(message)
        self.error_code = "MISSING_ENV_VAR"


__all__ = [
    "MSSSException",
    "AuthenticationError",
    "InvalidTokenError",
    "UnauthorizedError",
    "DocumentProcessingError",
    "UnsupportedFileTypeError",
    "FileSizeExceededError",
    "FileNotFoundError",
    "AnalysisError",
    "LLMError",
    "EmbeddingError",
    "ValidationError",
    "InvalidCredentialsError",
    "ConfigurationError",
    "MissingEnvironmentVariableError",
]
