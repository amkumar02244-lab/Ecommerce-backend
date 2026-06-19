from fastapi import APIRouter, Depends
from typing import List, Dict
from app.schemas.user import (
    UserResponse,
    UserUpdateRequest,
    StandardResponse
)
from app.services.user_service import user_service
from app.core.dependencies import (
    get_current_user,
    get_admin_user
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
def get_all_users(admin: Dict = Depends(get_admin_user)):
    """
    Get all users — ADMIN ONLY.

    In MuleSoft: HTTP Listener GET /users
    → JWT Validation Policy
    → Role check (admin only)
    → Database SELECT * FROM users
    """
    return user_service.get_all_users()


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: Dict = Depends(get_current_user)):
    """
    Get currently logged in user's own profile.
    Any logged in user can call this.

    No user_id needed — we extract it from JWT token.
    """
    from app.services.user_service import map_to_user_response
    return map_to_user_response(current_user)


@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: str, admin: Dict = Depends(get_admin_user)):
    """
    Get one user by ID — ADMIN ONLY.

    In MuleSoft: HTTP Listener GET /users/{user_id}
    → JWT Validation Policy
    → Role check
    → Database SELECT WHERE id = user_id
    """
    return user_service.get_user_by_id(user_id)


@router.put("/me", response_model=UserResponse)
def update_my_profile(
    request: UserUpdateRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Update currently logged in user's own profile.
    User can only update their own profile.

    Fields allowed to update:
    - first_name
    - last_name
    - phone
    - avatar_url
    """
    return user_service.update_user(current_user["id"], request)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    request: UserUpdateRequest,
    admin: Dict = Depends(get_admin_user)
):
    """
    Update any user by ID — ADMIN ONLY.
    """
    return user_service.update_user(user_id, request)


@router.delete("/{user_id}", response_model=StandardResponse)
def delete_user(user_id: str, admin: Dict = Depends(get_admin_user)):
    """
    Delete a user by ID — ADMIN ONLY.

    In MuleSoft: HTTP Listener DELETE /users/{user_id}
    → JWT Validation Policy
    → Role check
    → Database DELETE WHERE id = user_id
    """
    return user_service.delete_user(user_id)


@router.put("/{user_id}/block", response_model=StandardResponse)
def block_user(user_id: str, admin: Dict = Depends(get_admin_user)):
    """
    Block a user — ADMIN ONLY.
    Sets is_active = False so they cannot login.

    Blocked user gets 403 on next login attempt.
    """
    return user_service.block_user(user_id)