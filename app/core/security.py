from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import JWTError, jwt
from app.core.config import settings

import bcrypt

def hash_password(plain_password: str) -> str:
    """
    Convert plain text password to bcrypt hash.
    
    Example:
    "secret123" → "$2b$12$Kix9Y8JFTi1234abcXYZ..."
    
    This is ONE WAY — you can never reverse it back to "secret123"
    That's the point — even if CSV is stolen, passwords are safe
    """
    password_bytes = plain_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if a plain password matches a stored hash.
    
    Example:
    verify_password("secret123", "$2b$12$Kix9Y8JFTi1234abcXYZ...") → True
    verify_password("wrongpass", "$2b$12$Kix9Y8JFTi1234abcXYZ...") → False
    
    Used during login to verify user's password
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


# ─────────────────────────────────────────
# JWT TOKEN OPERATIONS
# ─────────────────────────────────────────

def create_access_token(data: Dict) -> str:
    """
    Generate a JWT access token.
    
    In MuleSoft: like generating an OAuth2 access token
    
    The token contains:
    - user_id    → who this token belongs to
    - role       → what they can access
    - exp        → when it expires (30 mins by default)
    
    Example token (3 parts separated by dots):
    eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiMTIzIn0.abc123
    header            .payload                    .signature
    """
    to_encode = data.copy()

    # Set expiry time
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode["exp"] = expire
    to_encode["type"] = "access"

    # Sign the token with our secret key
    # If anyone tampers with the token, verification will fail
    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return token


def create_refresh_token(data: Dict) -> str:
    """
    Generate a JWT refresh token.
    
    Refresh token lives longer (7 days) but can only be used
    to get a new access token — not to access protected routes.
    
    Flow:
    access token expires → client sends refresh token → get new access token
    Like re-authenticating silently without asking user to login again
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode["exp"] = expire
    to_encode["type"] = "refresh"

    token = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return token


def verify_token(token: str) -> Optional[Dict]:
    """
    Verify a JWT token and extract its payload.
    
    Returns the payload dict if valid, None if invalid/expired.
    
    In MuleSoft: like the JWT Validation policy in API Manager
    that checks every incoming request's Authorization header
    
    Example payload extracted:
    {
        "user_id": "f47ac10b-58cc-4372",
        "role": "customer",
        "exp": 1234567890,
        "type": "access"
    }
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        # Token is invalid, expired, or tampered with
        return None


def extract_user_id(token: str) -> Optional[str]:
    """
    Shortcut to get just the user_id from a token.
    Used in protected routes to know who is making the request.
    """
    payload = verify_token(token)
    if payload:
        return payload.get("user_id")
    return None