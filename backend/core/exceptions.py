"""
Custom exceptions for GitAnalyzer Pro
"""


class GitAnalyzerException(Exception):
    """Base exception for GitAnalyzer Pro"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class GitHubAPIException(GitAnalyzerException):
    """GitHub API related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=502)


class AIServiceException(GitAnalyzerException):
    """AI service related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=503)


class AnalysisException(GitAnalyzerException):
    """Analysis related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class ExportException(GitAnalyzerException):
    """Export related exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)


class ValidationException(GitAnalyzerException):
    """Input validation exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class NotFoundException(GitAnalyzerException):
    """Resource not found exceptions"""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)
