from pydantic import BaseModel, Field
from typing import Optional

# ─────────────────────────────────────────
# REQUEST SCHEMAS
# ─────────────────────────────────────────

class ProductCreateRequest(BaseModel):
    """
    Schema for POST /products — create a new product.
    Admin only.
    """
    name: str = Field(..., min_length=2, max_length=200)
    description: str = Field(..., min_length=10)
    price: float = Field(..., gt=0)         # gt=0 means must be greater than 0
    stock: int = Field(..., ge=0)           # ge=0 means must be 0 or more
    category: str = Field(..., min_length=2)
    image_url: Optional[str] = None
    brand: Optional[str] = None
    sku: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "iPhone 15 Pro",
                "description": "Latest Apple iPhone with A17 Pro chip",
                "price": 999.99,
                "stock": 50,
                "category": "Electronics",
                "brand": "Apple",
                "sku": "IPH-15-PRO-001"
            }
        }


class ProductUpdateRequest(BaseModel):
    """
    Schema for PUT /products/{id} — update a product.
    All fields optional — update only what's sent.
    Admin only.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    image_url: Optional[str] = None
    brand: Optional[str] = None
    sku: Optional[str] = None
    is_active: Optional[bool] = None


# ─────────────────────────────────────────
# RESPONSE SCHEMAS
# ─────────────────────────────────────────

class ProductResponse(BaseModel):
    """
    What we return when showing product data.
    This is what customers and admins see.
    """
    id: str
    name: str
    description: str
    price: float
    stock: int
    category: str
    is_active: bool
    image_url: Optional[str] = None
    brand: Optional[str] = None
    sku: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "name": "iPhone 15 Pro",
                "description": "Latest Apple iPhone with A17 Pro chip",
                "price": 999.99,
                "stock": 50,
                "category": "Electronics",
                "is_active": True,
                "brand": "Apple",
                "sku": "IPH-15-PRO-001",
                "created_at": "2024-01-01T10:00:00"
            }
        }