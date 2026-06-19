import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer
from app.core.database import Base

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False)
    product_id = Column(String, index=True, nullable=False)
    quantity = Column(Integer, default=1)
    
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, index=True, nullable=False)
    product_id = Column(String, index=True, nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)
    
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "price": self.price,
            "created_at": self.created_at
        }