from typing import Optional, List, Dict
from datetime import datetime
import uuid
from app.core.database import SessionLocal
from app.models.user import User

class UserRepository:

    def get_all(self) -> List[Dict]:
        with SessionLocal() as db:
            users = db.query(User).all()
            return [u.to_dict() for u in users]

    def get_by_id(self, user_id: str) -> Optional[Dict]:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            return user.to_dict() if user else None

    def get_by_email(self, email: str) -> Optional[Dict]:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
            return user.to_dict() if user else None

    def get_by_role(self, role: str) -> List[Dict]:
        with SessionLocal() as db:
            users = db.query(User).filter(User.role == role).all()
            return [u.to_dict() for u in users]

    def create(self, user_data: Dict) -> Dict:
        with SessionLocal() as db:
            # Auto-generate fields if missing
            if "id" not in user_data or not user_data["id"]:
                user_data["id"] = str(uuid.uuid4())
            if "created_at" not in user_data or not user_data["created_at"]:
                user_data["created_at"] = datetime.utcnow().isoformat()
            
            # Map string booleans if necessary
            if isinstance(user_data.get("is_active"), str):
                user_data["is_active"] = user_data["is_active"] == "True"
            if isinstance(user_data.get("is_verified"), str):
                user_data["is_verified"] = user_data["is_verified"] == "True"

            user = User(**user_data)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user.to_dict()

    def update(self, user_id: str, updated_data: Dict) -> Optional[Dict]:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return None
            
            # Map string booleans if necessary
            if "is_active" in updated_data and isinstance(updated_data["is_active"], str):
                updated_data["is_active"] = updated_data["is_active"] == "True"
            if "is_verified" in updated_data and isinstance(updated_data["is_verified"], str):
                updated_data["is_verified"] = updated_data["is_verified"] == "True"

            for key, value in updated_data.items():
                setattr(user, key, value)
            
            user.updated_at = datetime.utcnow().isoformat()
            db.commit()
            db.refresh(user)
            return user.to_dict()

    def delete(self, user_id: str) -> bool:
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return False
            db.delete(user)
            db.commit()
            return True

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def count_all(self) -> int:
        with SessionLocal() as db:
            return db.query(User).count()

user_repository = UserRepository()