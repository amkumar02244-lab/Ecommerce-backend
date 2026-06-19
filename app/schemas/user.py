from pydantic import BaseModel, EmailStr, Field
from typing import Optional

# Pydantic BaseModel = automatic validation
# If wrong data type comes in, FastAPI auto returns 422 error
# Just like MuleSoft's input validation / RAML type enforcement

# ─────────────────────────────────────────
# REQUEST SCHEMAS (what client sends TO us)
# ─────────────────────────────────────────

class UserRegisterRequest(BaseModel):
    """
    Schema for POST /auth/register
    Client must send exactly these fields — nothing more, nothing less.
    Pydantic will auto-validate types and required fields.
    
    In MuleSoft terms: this is your input payload validation in RAML
    """
    first_name: str = Field(..., min_length=2, max_length=50)
    last_name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr  # Auto validates email format e.g. must have @ and domain
    password: str = Field(..., min_length=6, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)

    class Config:
        # This lets us show example data in Swagger UI
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "password": "secret123",
                "phone": "9876543210"
            }
        }


class UserLoginRequest(BaseModel):
    """
    Schema for POST /auth/login
    Only needs email and password
    """
    email: EmailStr
    password: str = Field(..., min_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "password": "secret123"
            }
        }


class UserUpdateRequest(BaseModel):
    """
    Schema for PUT /users/{id}
    All fields optional — user can update one or all fields
    In MuleSoft terms: partial payload update (PATCH-style)
    """
    first_name: Optional[str] = Field(None, min_length=2, max_length=50)
    last_name: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None


# ──────────────────────────────────────────
# RESPONSE SCHEMAS (what we send BACK to client)
# ──────────────────────────────────────────

class UserResponse(BaseModel):
    """
    What we return when showing user data.
    Notice: NO password field here — never expose it!
    In MuleSoft: your output DataWeave transformation
    """
    id: str
    first_name: str
    last_name: str
    email: str
    role: str
    is_active: bool
    is_verified: bool
    phone: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "role": "customer",
                "is_active": True,
                "is_verified": False,
                "phone": "9876543210",
                "avatar_url": None,
                "created_at": "2024-01-01T10:00:00"
            }
        }


class UserLoginResponse(BaseModel):
    """
    What we return after successful login.
    Returns the token + basic user info.
    Token is like a MuleSoft OAuth2 access token.
    """
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class StandardResponse(BaseModel):
    """
    Generic response wrapper for success messages.
    Use this for operations like delete, block, verify etc.
    
    In MuleSoft: your standard success response structure
    """
    success: bool
    message: str
    data: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "User registered successfully",
                "data": None
            }
        }