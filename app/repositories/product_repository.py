from typing import Optional, List, Dict
from datetime import datetime
import uuid
from sqlalchemy import or_
from app.core.database import SessionLocal
from app.models.product import Product

class ProductRepository:

    def get_all(self) -> List[Dict]:
        with SessionLocal() as db:
            products = db.query(Product).all()
            return [p.to_dict() for p in products]

    def get_active(self) -> List[Dict]:
        with SessionLocal() as db:
            products = db.query(Product).filter(Product.is_active == True).all()
            return [p.to_dict() for p in products]

    def get_by_id(self, product_id: str) -> Optional[Dict]:
        with SessionLocal() as db:
            product = db.query(Product).filter(Product.id == product_id).first()
            return product.to_dict() if product else None

    def get_by_category(self, category: str) -> List[Dict]:
        with SessionLocal() as db:
            products = db.query(Product).filter(
                Product.category.ilike(category),
                Product.is_active == True
            ).all()
            return [p.to_dict() for p in products]

    def search(self, keyword: str) -> List[Dict]:
        with SessionLocal() as db:
            products = db.query(Product).filter(
                or_(
                    Product.name.ilike(f"%{keyword}%"),
                    Product.description.ilike(f"%{keyword}%")
                ),
                Product.is_active == True
            ).all()
            return [p.to_dict() for p in products]

    def sku_exists(self, sku: str) -> bool:
        if not sku:
            return False
        with SessionLocal() as db:
            return db.query(Product).filter(Product.sku == sku).first() is not None

    def create(self, product_data: Dict) -> Dict:
        with SessionLocal() as db:
            if "id" not in product_data or not product_data["id"]:
                product_data["id"] = str(uuid.uuid4())
            if "created_at" not in product_data or not product_data["created_at"]:
                product_data["created_at"] = datetime.utcnow().isoformat()
            
            # Map string booleans if necessary
            if isinstance(product_data.get("is_active"), str):
                product_data["is_active"] = product_data["is_active"] == "True"

            # Parse string stock to int if needed
            if "stock" in product_data and isinstance(product_data["stock"], str):
                product_data["stock"] = int(product_data["stock"])
            # Parse string price to float if needed
            if "price" in product_data and isinstance(product_data["price"], str):
                product_data["price"] = float(product_data["price"])

            product = Product(**product_data)
            db.add(product)
            db.commit()
            db.refresh(product)
            return product.to_dict()

    def update(self, product_id: str, updated_data: Dict) -> Optional[Dict]:
        with SessionLocal() as db:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return None
            
            # Map string booleans if necessary
            if "is_active" in updated_data and isinstance(updated_data["is_active"], str):
                updated_data["is_active"] = updated_data["is_active"] == "True"

            # Parse strings to numbers if needed
            if "stock" in updated_data and isinstance(updated_data["stock"], str):
                updated_data["stock"] = int(updated_data["stock"])
            if "price" in updated_data and isinstance(updated_data["price"], str):
                updated_data["price"] = float(updated_data["price"])

            for key, value in updated_data.items():
                setattr(product, key, value)
            
            product.updated_at = datetime.utcnow().isoformat()
            db.commit()
            db.refresh(product)
            return product.to_dict()

    def delete(self, product_id: str) -> bool:
        with SessionLocal() as db:
            product = db.query(Product).filter(Product.id == product_id).first()
            if not product:
                return False
            db.delete(product)
            db.commit()
            return True

    def count_all(self) -> int:
        with SessionLocal() as db:
            return db.query(Product).count()

    def count_active(self) -> int:
        with SessionLocal() as db:
            return db.query(Product).filter(Product.is_active == True).count()

product_repository = ProductRepository()