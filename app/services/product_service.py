from typing import List, Optional, Dict
from fastapi import HTTPException, status
from app.repositories.product_repository import product_repository
from app.schemas.product import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse
)
from app.schemas.user import StandardResponse


def map_to_product_response(product_dict: Dict) -> ProductResponse:
    """
    Convert raw CSV dict to ProductResponse schema.
    Handles type conversions — CSV stores everything as strings.

    In MuleSoft terms: output DataWeave transformation

    Raw CSV:
    {"price": "999.99", "stock": "50", "is_active": "True"}

    ProductResponse:
    {"price": 999.99, "stock": 50, "is_active": True}
    """
    return ProductResponse(
        id=product_dict["id"],
        name=product_dict["name"],
        description=product_dict["description"],
        # CSV stores numbers as strings — convert back to correct types
        price=float(product_dict["price"]),
        stock=int(product_dict["stock"]),
        category=product_dict["category"],
        is_active=product_dict["is_active"] == "True",
        image_url=product_dict.get("image_url") or None,
        brand=product_dict.get("brand") or None,
        sku=product_dict.get("sku") or None,
        created_at=product_dict.get("created_at")
    )


class ProductService:
    """
    Business logic for all product operations.

    Who can do what:
    - Customers → can view active products, search, filter
    - Admins    → can create, update, delete, view all
    """

    def create_product(self, request: ProductCreateRequest) -> ProductResponse:
        """
        Create a new product — ADMIN ONLY.

        Steps:
        1. Check SKU is unique (if provided)
        2. Build product data
        3. Save to CSV
        4. Return created product
        """

        # Step 1 — Check duplicate SKU
        if request.sku and product_repository.sku_exists(request.sku):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with SKU '{request.sku}' already exists"
            )

        # Step 2 — Build product data
        # CSV stores everything as strings
        # so we convert bool/float/int to string
        product_data = {
            "name": request.name,
            "description": request.description,
            "price": str(request.price),
            "stock": str(request.stock),
            "category": request.category,
            "is_active": "True",
            "image_url": request.image_url or "",
            "brand": request.brand or "",
            "sku": request.sku or ""
        }

        # Step 3 — Save to CSV
        created = product_repository.create(product_data)

        # Step 4 — Return response
        return map_to_product_response(created)

    def get_all_products(self, admin: bool = False) -> List[ProductResponse]:
        """
        Get all products.

        admin=True  → returns ALL products (including inactive)
        admin=False → returns only ACTIVE products (customers)

        In MuleSoft: choice router based on role
        """
        if admin:
            products = product_repository.get_all()
        else:
            products = product_repository.get_active()

        return [map_to_product_response(p) for p in products]

    def get_product_by_id(self, product_id: str) -> ProductResponse:
        """
        Get one product by ID.
        Both customers and admins can call this.
        """
        product = product_repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id '{product_id}' not found"
            )
        return map_to_product_response(product)

    def get_by_category(self, category: str) -> List[ProductResponse]:
        """
        Get all active products in a category.
        Customers use this to browse by category.
        """
        products = product_repository.get_by_category(category)
        return [map_to_product_response(p) for p in products]

    def search_products(self, keyword: str) -> List[ProductResponse]:
        """
        Search products by keyword in name or description.
        Customers use this for the search bar.
        """
        if len(keyword) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Search keyword must be at least 2 characters"
            )
        products = product_repository.search(keyword)
        return [map_to_product_response(p) for p in products]

    def update_product(
        self,
        product_id: str,
        request: ProductUpdateRequest
    ) -> ProductResponse:
        """
        Update a product — ADMIN ONLY.
        Only updates fields that were actually sent.
        """
        # Check product exists
        existing = product_repository.get_by_id(product_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # Check SKU uniqueness if SKU is being updated
        if request.sku and request.sku != existing.get("sku"):
            if product_repository.sku_exists(request.sku):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"SKU '{request.sku}' already in use"
                )

        # Only update fields that were sent
        update_data = {}
        if request.name is not None:
            update_data["name"] = request.name
        if request.description is not None:
            update_data["description"] = request.description
        if request.price is not None:
            update_data["price"] = str(request.price)
        if request.stock is not None:
            update_data["stock"] = str(request.stock)
        if request.category is not None:
            update_data["category"] = request.category
        if request.image_url is not None:
            update_data["image_url"] = request.image_url
        if request.brand is not None:
            update_data["brand"] = request.brand
        if request.sku is not None:
            update_data["sku"] = request.sku
        if request.is_active is not None:
            update_data["is_active"] = str(request.is_active)

        updated = product_repository.update(product_id, update_data)
        return map_to_product_response(updated)

    def delete_product(self, product_id: str) -> StandardResponse:
        """
        Delete a product — ADMIN ONLY.
        SQL: DELETE FROM products WHERE id = product_id
        """
        deleted = product_repository.delete(product_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        return StandardResponse(
            success=True,
            message="Product deleted successfully"
        )

    def toggle_active(
        self,
        product_id: str,
        is_active: bool
    ) -> StandardResponse:
        """
        Activate or deactivate a product — ADMIN ONLY.
        Deactivated products are hidden from customers.
        Like unpublishing a product without deleting it.
        """
        existing = product_repository.get_by_id(product_id)
        if not existing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        product_repository.update(product_id, {"is_active": str(is_active)})
        status_word = "activated" if is_active else "deactivated"
        return StandardResponse(
            success=True,
            message=f"Product {status_word} successfully"
        )


# Singleton instance
product_service = ProductService()