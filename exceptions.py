from fastapi import HTTPException

class LLMError(Exception):
    """Raised when the LLM call fails"""
    pass

class ValidationError(Exception):
    """Raised when LLM returns an unexpected value"""
    pass

class SessionError(Exception):
    """Raised when session operations fail"""
    pass