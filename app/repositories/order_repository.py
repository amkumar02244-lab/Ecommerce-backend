from typing import Optional, List, Dict
from app.core.database import (
    read_all,
    read_by_id,
    find_one,
    find_many,
    insert,
    update,
    delete,
    init_table
)
from app.models.order import (
    CART_TABLE, CART_COLUMNS,
    ORDER_TABLE, ORDER_COLUMNS,
    ORDER_ITEM_TABLE, ORDER_ITEM_COLUMNS
)

# Auto create all 3 CSV files on startup
init_table(CART_TABLE, CART_COLUMNS)
init_table(ORDER_TABLE, ORDER_COLUMNS)
init_table(ORDER_ITEM_TABLE, ORDER_ITEM_COLUMNS)


class OrderRepository:
    """
    Database operations for cart, orders and order items.

    3 tables:
    - cart_items.csv   → user's current cart
    - orders.csv       → placed orders
    - order_items.csv  → items inside each order
    """

    # ─────────────────────────────
    # CART OPERATIONS
    # ─────────────────────────────

    def get_cart_items(self, user_id: str) -> List[Dict]:
        """
        Get all cart items for a user.
        SQL: SELECT * FROM cart_items WHERE user_id = user_id
        """
        return find_many(CART_TABLE, "user_id", user_id)

    def get_cart_item(
        self,
        user_id: str,
        product_id: str
    ) -> Optional[Dict]:
        """
        Check if a product already exists in user's cart.
        SQL: SELECT * FROM cart_items
             WHERE user_id = user_id AND product_id = product_id
        Used to update quantity instead of adding duplicate.
        """
        items = self.get_cart_items(user_id)
        for item in items:
            if item.get("product_id") == product_id:
                return item
        return None

    def add_to_cart(self, cart_data: Dict) -> Dict:
        """
        Add a new item to cart.
        SQL: INSERT INTO cart_items VALUES (...)
        """
        return insert(CART_TABLE, cart_data)

    def update_cart_item(
        self,
        cart_item_id: str,
        updated_data: Dict
    ) -> Optional[Dict]:
        """
        Update cart item (usually quantity).
        SQL: UPDATE cart_items SET ... WHERE id = cart_item_id
        """
        return update(CART_TABLE, cart_item_id, updated_data)

    def remove_cart_item(self, cart_item_id: str) -> bool:
        """
        Remove one item from cart.
        SQL: DELETE FROM cart_items WHERE id = cart_item_id
        """
        return delete(CART_TABLE, cart_item_id)

    def clear_cart(self, user_id: str) -> None:
        """
        Remove ALL items from user's cart.
        Called after order is placed successfully.
        SQL: DELETE FROM cart_items WHERE user_id = user_id
        """
        items = self.get_cart_items(user_id)
        for item in items:
            delete(CART_TABLE, item["id"])

    # ─────────────────────────────
    # ORDER OPERATIONS
    # ─────────────────────────────

    def create_order(self, order_data: Dict) -> Dict:
        """
        Create a new order.
        SQL: INSERT INTO orders VALUES (...)
        """
        return insert(ORDER_TABLE, order_data)

    def get_order_by_id(self, order_id: str) -> Optional[Dict]:
        """
        Get one order by ID.
        SQL: SELECT * FROM orders WHERE id = order_id
        """
        return read_by_id(ORDER_TABLE, order_id)

    def get_orders_by_user(self, user_id: str) -> List[Dict]:
        """
        Get all orders for a user.
        SQL: SELECT * FROM orders WHERE user_id = user_id
        """
        return find_many(ORDER_TABLE, "user_id", user_id)

    def get_all_orders(self) -> List[Dict]:
        """
        Get all orders — admin only.
        SQL: SELECT * FROM orders
        """
        return read_all(ORDER_TABLE)

    def update_order_status(
        self,
        order_id: str,
        status: str
    ) -> Optional[Dict]:
        """
        Update order status.
        SQL: UPDATE orders SET status = status WHERE id = order_id
        """
        return update(ORDER_TABLE, order_id, {"status": status})

    # ─────────────────────────────
    # ORDER ITEMS OPERATIONS
    # ─────────────────────────────

    def add_order_item(self, item_data: Dict) -> Dict:
        """
        Add an item to an order.
        SQL: INSERT INTO order_items VALUES (...)
        Called once per product when order is created.
        """
        return insert(ORDER_ITEM_TABLE, item_data)

    def get_order_items(self, order_id: str) -> List[Dict]:
        """
        Get all items inside an order.
        SQL: SELECT * FROM order_items WHERE order_id = order_id
        """
        return find_many(ORDER_ITEM_TABLE, "order_id", order_id)


# Singleton instance
order_repository = OrderRepository()