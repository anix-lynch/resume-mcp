"""
Authentication middleware for Resume MCP
- Automatic auth for owner (via Vercel SSO or API key)
- Required auth for others (API key or token)
"""
import os
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

# Security scheme
security = HTTPBearer(auto_error=False)

# Get API keys from environment
OWNER_API_KEY = os.getenv("OWNER_API_KEY", "owner-secret-key-change-me")
PUBLIC_API_KEY = os.getenv("PUBLIC_API_KEY", "public-secret-key-change-me")

# Vercel deployment protection bypass (if enabled)
VERCEL_BYPASS_SECRET = os.getenv("VERCEL_BYPASS_SECRET", "")


def get_auth_token(request: Request) -> Optional[str]:
    """Extract auth token from request."""
    # Check Authorization header
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.replace("Bearer ", "")
    
    # Check X-API-Key header
    api_key = request.headers.get("X-API-Key", "")
    if api_key:
        return api_key
    
    # Check query parameter
    api_key = request.query_params.get("api_key", "")
    if api_key:
        return api_key
    
    # Check cookie
    api_key = request.cookies.get("api_key", "")
    if api_key:
        return api_key
    
    return None


def verify_owner_token(token: str) -> bool:
    """Verify if token belongs to owner."""
    return token == OWNER_API_KEY


def verify_public_token(token: str) -> bool:
    """Verify if token is valid public token."""
    return token == PUBLIC_API_KEY or token == OWNER_API_KEY


def is_owner(request: Request) -> bool:
    """Check if request is from owner (automatic auth)."""
    # Check for Vercel SSO (if deployment protection is enabled)
    vercel_user = request.headers.get("x-vercel-user", "")
    if vercel_user:
        # You can add your Vercel user ID here for automatic auth
        return True
    
    # Check for owner API key
    token = get_auth_token(request)
    if token and verify_owner_token(token):
        return True
    
    return False


def require_auth(request: Request, allow_public: bool = False) -> bool:
    """
    Require authentication for request.
    
    Args:
        request: FastAPI request
        allow_public: If True, allows unauthenticated access (for public endpoints)
    
    Returns:
        True if authenticated or public allowed, raises HTTPException otherwise
    """
    # Owner is always authenticated
    if is_owner(request):
        return True
    
    # If public access is allowed, no auth needed
    if allow_public:
        return True
    
    # Check for valid token
    token = get_auth_token(request)
    if token and verify_public_token(token):
        return True
    
    # No valid auth found
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required. Provide API key via header, query param, or cookie.",
        headers={"WWW-Authenticate": "Bearer"},
    )


def require_owner(request: Request) -> bool:
    """Require owner authentication."""
    if is_owner(request):
        return True
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Owner access required. This endpoint is restricted.",
    )

