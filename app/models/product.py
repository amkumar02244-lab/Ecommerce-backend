from dataclasses import dataclass
from typing import Optional

@dataclass
class Product:
    # Primary key
    id: str

    # Basic product info
    name: str
    description: str
    price: float
    stock: int                    # how many items available

    # Category — like Electronics, Clothing, Books etc
    category: str

    # Product status
    is_active: bool = True        # False = hidden from customers

    # Optional fields
    image_url: Optional[str] = None
    brand: Optional[str] = None
    sku: Optional[str] = None     # Stock Keeping Unit — unique product code

    # Timestamps
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


# CSV columns — order matters!
PRODUCT_COLUMNS = [
    "id",
    "name",
    "description",
    "price",
    "stock",
    "category",
    "is_active",
    "image_url",
    "brand",
    "sku",
    "created_at",
    "updated_at"
]

PRODUCT_TABLE = "products"