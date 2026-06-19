from dataclasses import dataclass
from typing import Optional

@dataclass
class CartItem:
    id: str
    user_id: str          # which user's cart
    product_id: str       # which product
    quantity: int         # how many
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class Order:
    id: str
    user_id: str          # who placed the order
    total_amount: float   # total price
    status: str           # pending, confirmed, shipped, delivered, cancelled
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

@dataclass
class OrderItem:
    id: str
    order_id: str         # which order this belongs to
    product_id: str       # which product
    quantity: int         # how many
    price: float          # price at time of purchase
    created_at: Optional[str] = None


# CSV columns
CART_COLUMNS = [
    "id", "user_id", "product_id",
    "quantity", "created_at", "updated_at"
]

ORDER_COLUMNS = [
    "id", "user_id", "total_amount",
    "status", "created_at", "updated_at"
]

ORDER_ITEM_COLUMNS = [
    "id", "order_id", "product_id",
    "quantity", "price", "created_at"
]

# Table names
CART_TABLE = "cart_items"
ORDER_TABLE = "orders"
ORDER_ITEM_TABLE = "order_items"