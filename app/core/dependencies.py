from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Optional
from app.core.security import verify_token
from app.repositories.user_repository import user_repository

bearer_scheme = HTTPBearer()
bearer_scheme_optional = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Dict:
    """
    Extract and verify the JWT token from request header.
    Returns the current logged-in user as a dict.

    In MuleSoft terms:
    - Depends() = like a before-flow interceptor
    - bearer_scheme = reads Authorization header
    - verify_token = like JWT Validation policy

    Usage in any protected route:
    @router.get("/profile")
    def get_profile(current_user = Depends(get_current_user)):
        return current_user
    """

    # Extract token from "Bearer eyJhbGci..." header
    token = credentials.credentials

    # Verify the token and extract payload
    payload = verify_token(token)

    # Token invalid or expired
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Extract user_id from token payload
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload invalid"
        )

    # Fetch fresh user data from CSV
    # We don't trust token data alone — always verify user still exists
    user = user_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )

    # Check account is still active
    # Admin may have blocked user after token was issued
    if user.get("is_active") != "True":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been blocked"
        )

    return user


def get_admin_user(
    current_user: Dict = Depends(get_current_user)
) -> Dict:
    """
    Same as get_current_user but ALSO checks if user is admin.
    Use this on admin-only endpoints.

    In MuleSoft terms:
    Like a choice router after JWT validation:
    role == "admin"? → continue
    role != "admin"? → raise 403

    Usage:
    @router.get("/admin/users")
    def list_users(admin = Depends(get_admin_user)):
        return all users
    """
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def get_verified_user(
    current_user: Dict = Depends(get_current_user)
) -> Dict:
    """
    Same as get_current_user but ALSO checks email is verified.
    Use this on endpoints that require verified accounts.

    Example: placing an order requires verified email
    """
    if current_user.get("is_verified") != "True":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email first"
        )
    return current_user


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme_optional)
) -> Optional[Dict]:
    """
    Extract and verify the JWT token if present.
    If no token is sent or if the token is invalid, returns None instead of raising an error.
    Used for endpoints that are public but have optional logged-in behavior.
    """
    if not credentials:
        return None
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        return None
    user_id = payload.get("user_id")
    if not user_id:
        return None
    user = user_repository.get_by_id(user_id)
    if not user:
        return None
    if user.get("is_active") != "True":
        return None
    return user