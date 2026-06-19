from pydantic import BaseModel, Field
from typing import Optional, List

# ─────────────────────────────
# CART SCHEMAS
# ─────────────────────────────

class AddToCartRequest(BaseModel):
    """
    POST /cart/add
    Add a product to cart or increase quantity.
    """
    product_id: str
    quantity: int = Field(..., ge=1, description="Must be at least 1")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "quantity": 2
            }
        }


class CartItemResponse(BaseModel):
    """
    What a cart item looks like in response.
    Includes product details for display.
    """
    id: str
    product_id: str
    product_name: str       # fetched from products CSV
    product_price: float    # fetched from products CSV
    quantity: int
    subtotal: float         # price × quantity


class CartResponse(BaseModel):
    """
    Full cart response with all items and total.
    """
    items: List[CartItemResponse]
    total: float
    item_count: int


# ─────────────────────────────
# ORDER SCHEMAS
# ─────────────────────────────

class CreateOrderRequest(BaseModel):
    """
    POST /orders/create
    Convert cart items into an order.
    """
    notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "notes": "Please deliver after 6pm"
            }
        }


class DirectCreateOrderRequest(BaseModel):
    """
    POST /admin/orders/direct-create
    For AI Agent to create orders without a cart.
    """
    customer_phone: str
    customer_name: str
    product_id: str
    quantity: int = Field(1, ge=1)
    address: Optional[str] = None
    color: Optional[str] = None
    size: Optional[str] = None

class OrderItemResponse(BaseModel):
    """Single item inside an order."""
    id: str
    product_id: str
    product_name: str
    quantity: int
    price: float
    subtotal: float


class OrderResponse(BaseModel):
    """Full order with all items."""
    id: str
    user_id: str
    total_amount: float
    status: str
    items: List[OrderItemResponse]
    created_at: Optional[str] = None


class UpdateOrderStatusRequest(BaseModel):
    """
    PUT /orders/status/{id} — ADMIN ONLY.
    Update order status.
    """
    status: str = Field(
        ...,
        description="pending | confirmed | shipped | delivered | cancelled"
    )

    class Config:
        json_schema_extra = {
            "example": {"status": "confirmed"}
        }