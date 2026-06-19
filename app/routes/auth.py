from fastapi import APIRouter, Depends
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserResponse,
    UserLoginResponse,
    StandardResponse
)
from app.services.user_service import user_service
from app.core.dependencies import get_current_user
from typing import Dict

# APIRouter = like a MuleSoft sub-flow or API Kit router
# prefix    = all routes in this file start with /auth
# tags      = groups endpoints together in Swagger UI
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=StandardResponse, status_code=201)
def register(request: UserRegisterRequest):
    """
    Register a new user account.

    - Validates input automatically via Pydantic
    - Checks for duplicate email
    - Hashes password before storing
    - Returns success message with user_id

    In MuleSoft: HTTP Listener POST /auth/register → flow → DB insert
    """
    return user_service.register(request)


@router.post("/login", response_model=UserLoginResponse)
def login(request: UserLoginRequest):
    """
    Login with email and password.

    - Verifies email exists
    - Verifies password against hash
    - Checks account is active
    - Returns JWT access token + user info

    The access_token must be sent in header for all protected routes:
    Authorization: Bearer <access_token>
    """
    return user_service.login(request)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: Dict = Depends(get_current_user)):
    """
    Get currently logged in user's profile.

    This is a PROTECTED route — requires valid JWT token.
    
    In MuleSoft: HTTP Listener GET /auth/me 
    → JWT Validation Policy intercepts
    → flow gets user info

    How to call:
    GET /auth/me
    Header: Authorization: Bearer eyJhbGci...
    """
    # current_user is injected by get_current_user dependency
    # it's already fetched and verified — just map and return
    from app.services.user_service import map_to_user_response
    return map_to_user_response(current_user)