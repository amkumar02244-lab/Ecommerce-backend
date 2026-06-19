from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Optional
from app.schemas.product import (
    ProductCreateRequest,
    ProductUpdateRequest,
    ProductResponse
)
from app.schemas.user import StandardResponse
from app.services.product_service import product_service
from app.core.dependencies import (
    get_optional_user,
    get_admin_user
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(
    request: ProductCreateRequest,
    admin: Dict = Depends(get_admin_user)
):
    """
    Create a new product — ADMIN ONLY.
    POST /products
    """
    return product_service.create_product(request)


@router.get("/", response_model=List[ProductResponse])
def get_all_products(
    current_user: Optional[Dict] = Depends(get_optional_user)
):
    """
    Get all products.
    - Admin → sees ALL products including inactive
    - Customer → sees only ACTIVE products

    GET /products
    """
    is_admin = current_user.get("role") == "admin" if current_user else False
    return product_service.get_all_products(admin=is_admin)


@router.get("/search", response_model=List[ProductResponse])
def search_products(
    # Query parameter: GET /products/search?keyword=iphone
    keyword: str = Query(..., min_length=2, description="Search keyword")
):
    """
    Search products by name or description.
    GET /products/search?keyword=iphone

    In MuleSoft: query parameter in HTTP Listener
    like #[attributes.queryParams.keyword]
    """
    return product_service.search_products(keyword)


@router.get("/category/{category}", response_model=List[ProductResponse])
def get_by_category(category: str):
    """
    Get all active products in a category.
    GET /products/category/Electronics

    In MuleSoft: URI parameter
    like #[attributes.uriParams.category]
    """
    return product_service.get_by_category(category)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str):
    """
    Get one product by ID.
    GET /products/{product_id}
    Both customers and admins can access.
    """
    return product_service.get_product_by_id(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    request: ProductUpdateRequest,
    admin: Dict = Depends(get_admin_user)
):
    """
    Update a product — ADMIN ONLY.
    PUT /products/{product_id}
    """
    return product_service.update_product(product_id, request)


@router.delete("/{product_id}", response_model=StandardResponse)
def delete_product(
    product_id: str,
    admin: Dict = Depends(get_admin_user)
):
    """
    Delete a product — ADMIN ONLY.
    DELETE /products/{product_id}
    """
    return product_service.delete_product(product_id)


@router.put("/{product_id}/toggle", response_model=StandardResponse)
def toggle_product(
    product_id: str,
    is_active: bool = Query(..., description="True to activate, False to deactivate"),
    admin: Dict = Depends(get_admin_user)
):
    """
    Activate or deactivate a product — ADMIN ONLY.
    PUT /products/{product_id}/toggle?is_active=false

    Use this instead of deleting —
    deactivated products are hidden from customers
    but data is preserved.
    """
    return product_service.toggle_active(product_id, is_active)