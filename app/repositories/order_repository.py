from typing import Optional, List, Dict
from datetime import datetime
import uuid
from app.core.database import SessionLocal
from app.models.order import CartItem, Order, OrderItem

class OrderRepository:

    # ─────────────────────────────
    # CART OPERATIONS
    # ─────────────────────────────

    def get_cart_items(self, user_id: str) -> List[Dict]:
        with SessionLocal() as db:
            items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
            return [i.to_dict() for i in items]

    def get_cart_item(self, user_id: str, product_id: str) -> Optional[Dict]:
        with SessionLocal() as db:
            item = db.query(CartItem).filter(
                CartItem.user_id == user_id, 
                CartItem.product_id == product_id
            ).first()
            return item.to_dict() if item else None

    def add_to_cart(self, cart_data: Dict) -> Dict:
        with SessionLocal() as db:
            if "id" not in cart_data or not cart_data["id"]:
                cart_data["id"] = str(uuid.uuid4())
            if "created_at" not in cart_data or not cart_data["created_at"]:
                cart_data["created_at"] = datetime.utcnow().isoformat()
            
            if "quantity" in cart_data and isinstance(cart_data["quantity"], str):
                cart_data["quantity"] = int(cart_data["quantity"])

            item = CartItem(**cart_data)
            db.add(item)
            db.commit()
            db.refresh(item)
            return item.to_dict()

    def update_cart_item(self, cart_item_id: str, updated_data: Dict) -> Optional[Dict]:
        with SessionLocal() as db:
            item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
            if not item:
                return None
            
            if "quantity" in updated_data and isinstance(updated_data["quantity"], str):
                updated_data["quantity"] = int(updated_data["quantity"])

            for key, value in updated_data.items():
                setattr(item, key, value)
            
            item.updated_at = datetime.utcnow().isoformat()
            db.commit()
            db.refresh(item)
            return item.to_dict()

    def remove_cart_item(self, cart_item_id: str) -> bool:
        with SessionLocal() as db:
            item = db.query(CartItem).filter(CartItem.id == cart_item_id).first()
            if not item:
                return False
            db.delete(item)
            db.commit()
            return True

    def clear_cart(self, user_id: str) -> None:
        with SessionLocal() as db:
            db.query(CartItem).filter(CartItem.user_id == user_id).delete()
            db.commit()

    # ─────────────────────────────
    # ORDER OPERATIONS
    # ─────────────────────────────

    def create_order(self, order_data: Dict) -> Dict:
        with SessionLocal() as db:
            if "id" not in order_data or not order_data["id"]:
                order_data["id"] = str(uuid.uuid4())
            if "created_at" not in order_data or not order_data["created_at"]:
                order_data["created_at"] = datetime.utcnow().isoformat()
                
            if "total_amount" in order_data and isinstance(order_data["total_amount"], str):
                order_data["total_amount"] = float(order_data["total_amount"])

            order = Order(**order_data)
            db.add(order)
            db.commit()
            db.refresh(order)
            return order.to_dict()

    def get_order_by_id(self, order_id: str) -> Optional[Dict]:
        with SessionLocal() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            return order.to_dict() if order else None

    def get_orders_by_user(self, user_id: str) -> List[Dict]:
        with SessionLocal() as db:
            orders = db.query(Order).filter(Order.user_id == user_id).all()
            return [o.to_dict() for o in orders]

    def get_all_orders(self) -> List[Dict]:
        with SessionLocal() as db:
            orders = db.query(Order).all()
            return [o.to_dict() for o in orders]

    def update_order_status(self, order_id: str, status: str) -> Optional[Dict]:
        with SessionLocal() as db:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return None
            order.status = status
            order.updated_at = datetime.utcnow().isoformat()
            db.commit()
            db.refresh(order)
            return order.to_dict()

    # ─────────────────────────────
    # ORDER ITEMS OPERATIONS
    # ─────────────────────────────

    def add_order_item(self, item_data: Dict) -> Dict:
        with SessionLocal() as db:
            if "id" not in item_data or not item_data["id"]:
                item_data["id"] = str(uuid.uuid4())
            if "created_at" not in item_data or not item_data["created_at"]:
                item_data["created_at"] = datetime.utcnow().isoformat()
                
            if "quantity" in item_data and isinstance(item_data["quantity"], str):
                item_data["quantity"] = int(item_data["quantity"])
            if "price" in item_data and isinstance(item_data["price"], str):
                item_data["price"] = float(item_data["price"])

            item = OrderItem(**item_data)
            db.add(item)
            db.commit()
            db.refresh(item)
            return item.to_dict()

    def get_order_items(self, order_id: str) -> List[Dict]:
        with SessionLocal() as db:
            items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
            return [i.to_dict() for i in items]

order_repository = OrderRepository()