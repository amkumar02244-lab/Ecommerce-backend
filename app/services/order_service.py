from typing import List, Dict
from fastapi import HTTPException, status
from app.repositories.order_repository import order_repository
from app.repositories.product_repository import product_repository
from app.schemas.order import (
    AddToCartRequest,
    CartItemResponse,
    CartResponse,
    CreateOrderRequest,
    OrderItemResponse,
    OrderResponse,
    UpdateOrderStatusRequest
)
from app.schemas.user import StandardResponse

VALID_STATUSES = ["pending", "confirmed", "shipped", "delivered", "cancelled"]


class OrderService:

    def add_to_cart(self, user_id: str, request: AddToCartRequest) -> CartItemResponse:
        product = product_repository.get_by_id(request.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        if product.get("is_active") != "True":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is not available"
            )
        available_stock = int(product.get("stock", 0))
        if available_stock < request.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {available_stock} items available in stock"
            )
        existing_item = order_repository.get_cart_item(user_id, request.product_id)
        if existing_item:
            new_quantity = int(existing_item["quantity"]) + request.quantity
            if new_quantity > available_stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Cannot add {request.quantity} more. Only {available_stock} in stock"
                )
            updated = order_repository.update_cart_item(
                existing_item["id"],
                {"quantity": str(new_quantity)}
            )
            cart_item = updated
        else:
            cart_data = {
                "user_id": user_id,
                "product_id": request.product_id,
                "quantity": str(request.quantity)
            }
            cart_item = order_repository.add_to_cart(cart_data)

        price = float(product["price"])
        qty = int(cart_item["quantity"])
        return CartItemResponse(
            id=cart_item["id"],
            product_id=request.product_id,
            product_name=product["name"],
            product_price=price,
            quantity=qty,
            subtotal=round(price * qty, 2)
        )

    def get_cart(self, user_id: str) -> CartResponse:
        cart_items = order_repository.get_cart_items(user_id)
        response_items = []
        total = 0.0
        for item in cart_items:
            product = product_repository.get_by_id(item["product_id"])
            if not product:
                continue
            price = float(product["price"])
            qty = int(item["quantity"])
            subtotal = round(price * qty, 2)
            total += subtotal
            response_items.append(CartItemResponse(
                id=item["id"],
                product_id=item["product_id"],
                product_name=product["name"],
                product_price=price,
                quantity=qty,
                subtotal=subtotal
            ))
        return CartResponse(
            items=response_items,
            total=round(total, 2),
            item_count=len(response_items)
        )

    def remove_from_cart(self, user_id: str, cart_item_id: str) -> StandardResponse:
        cart_items = order_repository.get_cart_items(user_id)
        item_ids = [i["id"] for i in cart_items]
        if cart_item_id not in item_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )
        order_repository.remove_cart_item(cart_item_id)
        return StandardResponse(
            success=True,
            message="Item removed from cart"
        )

    def create_order(self, user_id: str, request: CreateOrderRequest) -> OrderResponse:
        cart_items = order_repository.get_cart_items(user_id)
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your cart is empty"
            )
        total = 0.0
        validated_items = []
        for item in cart_items:
            product = product_repository.get_by_id(item["product_id"])
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product no longer exists"
                )
            if product.get("is_active") != "True":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product '{product['name']}' is no longer available"
                )
            qty = int(item["quantity"])
            stock = int(product.get("stock", 0))
            if stock < qty:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Only {stock} of '{product['name']}' available"
                )
            price = float(product["price"])
            subtotal = round(price * qty, 2)
            total += subtotal
            validated_items.append({
                "product": product,
                "cart_item": item,
                "quantity": qty,
                "price": price,
                "subtotal": subtotal
            })
        order_data = {
            "user_id": user_id,
            "total_amount": str(round(total, 2)),
            "status": "pending"
        }
        order = order_repository.create_order(order_data)
        order_items_response = []
        for v in validated_items:
            order_item = order_repository.add_order_item({
                "order_id": order["id"],
                "product_id": v["product"]["id"],
                "quantity": str(v["quantity"]),
                "price": str(v["price"])
            })
            new_stock = int(v["product"]["stock"]) - v["quantity"]
            product_repository.update(
                v["product"]["id"],
                {"stock": str(new_stock)}
            )
            order_items_response.append(OrderItemResponse(
                id=order_item["id"],
                product_id=v["product"]["id"],
                product_name=v["product"]["name"],
                quantity=v["quantity"],
                price=v["price"],
                subtotal=v["subtotal"]
            ))
        order_repository.clear_cart(user_id)
        return OrderResponse(
            id=order["id"],
            user_id=user_id,
            total_amount=round(total, 2),
            status="pending",
            items=order_items_response,
            created_at=order.get("created_at")
        )

    def get_my_orders(self, user_id: str) -> List[OrderResponse]:
        orders = order_repository.get_orders_by_user(user_id)
        return [self._build_order_response(o) for o in orders]

    def get_order_by_id(self, order_id: str, user_id: str = None) -> OrderResponse:
        order = order_repository.get_order_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found"
            )
        if user_id and order.get("user_id") != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have access to this order"
            )
        return self._build_order_response(order)

    def get_all_orders(self) -> List[OrderResponse]:
        orders = order_repository.get_all_orders()
        return [self._build_order_response(o) for o in orders]

    def update_order_status(self, order_id: str, request: UpdateOrderStatusRequest) -> StandardResponse:
        print(f"[DEBUG] Updating order: {order_id}")
        print(f"[DEBUG] New status: {request.status}")
        if request.status not in VALID_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status. Must be one of: {VALID_STATUSES}"
            )
        order = order_repository.get_order_by_id(order_id)
        print(f"[DEBUG] Found order: {order}")
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order not found with id: {order_id}"
            )
        order_repository.update_order_status(order_id, request.status)
        return StandardResponse(
            success=True,
            message=f"Order status updated to '{request.status}'"
        )

    def _build_order_response(self, order: Dict) -> OrderResponse:
        order_items = order_repository.get_order_items(order["id"])
        items_response = []
        for item in order_items:
            product = product_repository.get_by_id(item["product_id"])
            product_name = product["name"] if product else "Deleted Product"
            price = float(item["price"])
            qty = int(item["quantity"])
            items_response.append(OrderItemResponse(
                id=item["id"],
                product_id=item["product_id"],
                product_name=product_name,
                quantity=qty,
                price=price,
                subtotal=round(price * qty, 2)
            ))
        return OrderResponse(
            id=order["id"],
            user_id=order["user_id"],
            total_amount=float(order["total_amount"]),
            status=order["status"],
            items=items_response,
            created_at=order.get("created_at")
        )


order_service = OrderService()