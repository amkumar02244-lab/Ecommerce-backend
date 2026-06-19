import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="customer")
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    phone = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())
    updated_at = Column(String, nullable=True)

    def to_dict(self):
        """Convert ORM object to dictionary for backward compatibility with services"""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "role": self.role,
            "is_active": str(self.is_active), # Keep "True"/"False" string for backward compatibility
            "is_verified": str(self.is_verified),
            "phone": self.phone,
            "avatar_url": self.avatar_url,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }