from fastapi import APIRouter, Depends
from typing import List, Dict
from app.schemas.order import (
    AddToCartRequest,
    CartResponse,
    CartItemResponse,
    CreateOrderRequest,
    OrderResponse,
    UpdateOrderStatusRequest
)
from app.schemas.user import StandardResponse
from app.services.order_service import order_service
from app.core.dependencies import (
    get_current_user,
    get_admin_user
)

router = APIRouter(tags=["Cart & Orders"])


# ─────────────────────────────
# CART ENDPOINTS
# ─────────────────────────────

@router.post("/cart/add", response_model=CartItemResponse, status_code=201)
def add_to_cart(
    request: AddToCartRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Add a product to cart.
    If already in cart → quantity is increased.

    POST /cart/add
    Requires: logged in user
    """
    return order_service.add_to_cart(current_user["id"], request)


@router.get("/cart", response_model=CartResponse)
def get_cart(current_user: Dict = Depends(get_current_user)):
    """
    Get current user's cart with all items and total.

    GET /cart
    Requires: logged in user
    """
    return order_service.get_cart(current_user["id"])


@router.delete("/cart/remove/{cart_item_id}", response_model=StandardResponse)
def remove_from_cart(
    cart_item_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Remove one item from cart.

    DELETE /cart/remove/{cart_item_id}
    Requires: logged in user
    Security: can only remove your own cart items
    """
    return order_service.remove_from_cart(
        current_user["id"],
        cart_item_id
    )


# ─────────────────────────────
# ORDER ENDPOINTS
# ─────────────────────────────

@router.post("/orders/create", response_model=OrderResponse, status_code=201)
def create_order(
    request: CreateOrderRequest,
    current_user: Dict = Depends(get_current_user)
):
    """
    Convert cart into a real order.

    POST /orders/create
    Requires: logged in user

    What happens:
    1. Cart items → order record
    2. Stock reduced per product
    3. Cart cleared automatically
    """
    return order_service.create_order(current_user["id"], request)


@router.get("/orders", response_model=List[OrderResponse])
def get_my_orders(current_user: Dict = Depends(get_current_user)):
    """
    Get all orders for logged in user.

    GET /orders
    Requires: logged in user
    """
    return order_service.get_my_orders(current_user["id"])


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get one order by ID.
    Users can only see their own orders.

    GET /orders/{order_id}
    Requires: logged in user
    """
    return order_service.get_order_by_id(
        order_id,
        user_id=current_user["id"]
    )


# ─────────────────────────────
# ADMIN ORDER ENDPOINTS
# ─────────────────────────────

@router.get("/admin/orders", response_model=List[OrderResponse])
def get_all_orders(admin: Dict = Depends(get_admin_user)):
    """
    Get ALL orders across all users — ADMIN ONLY.

    GET /admin/orders
    Requires: admin role
    """
    return order_service.get_all_orders()


@router.put("/admin/orders/{order_id}/status", response_model=StandardResponse)
def update_order_status(
    order_id: str,
    request: UpdateOrderStatusRequest,
    admin: Dict = Depends(get_admin_user)
):
    """
    Update order status — ADMIN ONLY.

    PUT /orders/status/{order_id}
    Requires: admin role

    Valid statuses:
    pending → confirmed → shipped → delivered
    any     → cancelled
    """
    return order_service.update_order_status(order_id, request)