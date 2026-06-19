from typing import Optional, Dict, List
from app.repositories.user_repository import user_repository
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    UserUpdateRequest,
    UserResponse,
    UserLoginResponse,
    StandardResponse
)
from fastapi import HTTPException, status


def map_to_user_response(user_dict: Dict) -> UserResponse:
    """
    Convert raw CSV dict to UserResponse schema.
    This strips out password and maps types correctly.

    In MuleSoft terms: your output DataWeave transformation
    
    Raw CSV dict looks like:
    {"id": "abc", "email": "j@j.com", "password": "$2b$...", "is_active": "True"}
    
    UserResponse looks like:
    {"id": "abc", "email": "j@j.com", "is_active": True}  ← no password, bool not string
    """
    return UserResponse(
        id=user_dict["id"],
        first_name=user_dict["first_name"],
        last_name=user_dict["last_name"],
        email=user_dict["email"],
        role=user_dict["role"],
        # CSV stores everything as strings
        # so "True"/"False" strings need to be converted to bool
        is_active=user_dict["is_active"] == "True",
        is_verified=user_dict["is_verified"] == "True",
        phone=user_dict.get("phone") or None,
        avatar_url=user_dict.get("avatar_url") or None,
        created_at=user_dict.get("created_at")
    )


class UserService:
    """
    Business logic for all user operations.
    
    In MuleSoft terms: this is your main flow logic
    between the HTTP Listener and Database Connector.
    """

    def register(self, request: UserRegisterRequest) -> StandardResponse:
        """
        Register a new user.
        
        Steps:
        1. Check if email already exists
        2. Hash the password
        3. Save to CSV
        4. Return success response
        """

        # Step 1 — Check duplicate email
        # Like a MuleSoft choice router checking a condition
        if user_repository.email_exists(request.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Step 2 — Build user data dict
        user_data = {
            "first_name": request.first_name,
            "last_name": request.last_name,
            "email": request.email.lower(),  # always store email in lowercase
            "password": hash_password(request.password),  # NEVER store plain text
            "role": "customer",       # default role
            "is_active": "True",      # CSV stores as string
            "is_verified": "False",   # email not verified yet
            "phone": request.phone or "",
            "avatar_url": ""
        }

        # Step 3 — Save to CSV
        # repository handles id and created_at auto generation
        created_user = user_repository.create(user_data)

        # Step 4 — Return success
        return StandardResponse(
            success=True,
            message="User registered successfully",
            data={"user_id": created_user["id"]}
        )

    def login(self, request: UserLoginRequest) -> UserLoginResponse:
        """
        Login a user.
        
        Steps:
        1. Find user by email
        2. Verify password
        3. Check account is active
        4. Generate JWT tokens
        5. Return tokens + user info
        """

        # Step 1 — Find user by email
        user = user_repository.get_by_email(request.email.lower())
        if not user:
            # Don't say "email not found" — that reveals which emails exist
            # Always say generic message for security
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Step 2 — Verify password
        if not verify_password(request.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Step 3 — Check account is active
        if user["is_active"] != "True":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account has been blocked. Contact support."
            )

        # Step 4 — Generate JWT tokens
        token_data = {
            "user_id": user["id"],
            "role": user["role"]
        }
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)

        # Step 5 — Return tokens + user info
        return UserLoginResponse(
            access_token=access_token,
            token_type="bearer",
            user=map_to_user_response(user)
        )

    def get_all_users(self) -> List[UserResponse]:
        """
        Get all users — admin only.
        SQL: SELECT * FROM users
        """
        users = user_repository.get_all()
        return [map_to_user_response(u) for u in users]

    def get_user_by_id(self, user_id: str) -> UserResponse:
        """
        Get one user by ID.
        SQL: SELECT * FROM users WHERE id = user_id
        """
        user = user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return map_to_user_response(user)

    def update_user(self, user_id: str, request: UserUpdateRequest) -> UserResponse:
        """
        Update user profile.
        SQL: UPDATE users SET ... WHERE id = user_id
        """
        # Check user exists first
        existing = user_repository.get_by_id(user_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Only update fields that were actually sent
        # exclude_none=True means don't include fields the client didn't send
        update_data = request.model_dump(exclude_none=True)

        updated = user_repository.update(user_id, update_data)
        return map_to_user_response(updated)

    def delete_user(self, user_id: str) -> StandardResponse:
        """
        Delete a user by ID — admin only.
        SQL: DELETE FROM users WHERE id = user_id
        """
        deleted = user_repository.delete(user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return StandardResponse(
            success=True,
            message="User deleted successfully"
        )

    def block_user(self, user_id: str) -> StandardResponse:
        """
        Block a user — admin only.
        Sets is_active to False so they can't login.
        """
        existing = user_repository.get_by_id(user_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user_repository.update(user_id, {"is_active": "False"})
        return StandardResponse(
            success=True,
            message="User blocked successfully"
        )


# Singleton instance
user_service = UserService()