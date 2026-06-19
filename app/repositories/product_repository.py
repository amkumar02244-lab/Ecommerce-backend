from typing import Optional, List, Dict
from app.core.database import (
    read_all,
    read_by_id,
    find_one,
    insert,
    update,
    delete,
    init_table
)
from app.models.product import PRODUCT_TABLE, PRODUCT_COLUMNS

# Auto create data/products.csv on startup
init_table(PRODUCT_TABLE, PRODUCT_COLUMNS)


class ProductRepository:
    """
    All database operations for the Product table.
    SQL equivalent operations shown for each method.

    In MuleSoft terms: Database Connector operations
    for the products table.
    """

    def get_all(self) -> List[Dict]:
        """
        Get all products.
        SQL: SELECT * FROM products
        """
        return read_all(PRODUCT_TABLE)

    def get_active(self) -> List[Dict]:
        """
        Get only active products.
        SQL: SELECT * FROM products WHERE is_active = 'True'

        Customers should only see active products.
        Admin can see all including inactive.
        """
        products = read_all(PRODUCT_TABLE)
        return [p for p in products if p.get("is_active") == "True"]

    def get_by_id(self, product_id: str) -> Optional[Dict]:
        """
        Get one product by ID.
        SQL: SELECT * FROM products WHERE id = product_id
        """
        return read_by_id(PRODUCT_TABLE, product_id)

    def get_by_category(self, category: str) -> List[Dict]:
        """
        Get all products in a category.
        SQL: SELECT * FROM products WHERE category = category
        """
        products = read_all(PRODUCT_TABLE)
        return [
            p for p in products
            if p.get("category", "").lower() == category.lower()
            and p.get("is_active") == "True"
        ]

    def search(self, keyword: str) -> List[Dict]:
        """
        Search products by name or description.
        SQL: SELECT * FROM products
             WHERE name LIKE '%keyword%'
             OR description LIKE '%keyword%'

        CSV doesn't support LIKE queries so we
        do it manually in Python — same result.
        """
        keyword_lower = keyword.lower()
        products = read_all(PRODUCT_TABLE)
        return [
            p for p in products
            if keyword_lower in p.get("name", "").lower()
            or keyword_lower in p.get("description", "").lower()
            and p.get("is_active") == "True"
        ]

    def sku_exists(self, sku: str) -> bool:
        """
        Check if a SKU already exists.
        SQL: SELECT COUNT(*) FROM products WHERE sku = sku
        Prevents duplicate product codes.
        """
        if not sku:
            return False
        return find_one(PRODUCT_TABLE, "sku", sku) is not None

    def create(self, product_data: Dict) -> Dict:
        """
        Insert a new product.
        SQL: INSERT INTO products VALUES (...)
        """
        return insert(PRODUCT_TABLE, product_data)

    def update(self, product_id: str, updated_data: Dict) -> Optional[Dict]:
        """
        Update a product by ID.
        SQL: UPDATE products SET ... WHERE id = product_id
        """
        return update(PRODUCT_TABLE, product_id, updated_data)

    def delete(self, product_id: str) -> bool:
        """
        Delete a product by ID.
        SQL: DELETE FROM products WHERE id = product_id
        """
        return delete(PRODUCT_TABLE, product_id)

    def count_all(self) -> int:
        """
        Count total products.
        SQL: SELECT COUNT(*) FROM products
        Used by admin dashboard for stats.
        """
        return len(read_all(PRODUCT_TABLE))

    def count_active(self) -> int:
        """
        Count active products only.
        SQL: SELECT COUNT(*) FROM products WHERE is_active = 'True'
        """
        return len(self.get_active())


# Singleton instance
product_repository = ProductRepository()