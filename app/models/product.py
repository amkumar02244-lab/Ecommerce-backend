import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    image_url = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    sku = Column(String, nullable=True, unique=True, index=True)
    
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "is_active": str(self.is_active),
            "image_url": self.image_url,
            "brand": self.brand,
            "sku": self.sku,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }