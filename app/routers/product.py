from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.dependency import get_current_user, require_roles
from app.schemas import (
    CreateProductIn,
    CreateReviewIn,
    ProductSchema,
    ReviewSchema,
    UpdateProductIn,
    UserSchema,
)
from app.services import ProductService, ReviewService
from app.tools import UserRole

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductSchema])
async def all_products(product_service: Annotated[ProductService, Depends()]):
    return await product_service.get_all_products()


@router.post("", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_service: Annotated[ProductService, Depends()],
    product: CreateProductIn,
    current_user: Annotated[
        UserSchema, Depends(require_roles((UserRole.ADMIN, UserRole.SUPPLIER)))
    ],
):
    return await product_service.create_product(product, current_user)


@router.get("/{category_slug}", response_model=list[ProductSchema])
async def product_by_category(
    product_service: Annotated[ProductService, Depends()], category_slug: str
):
    return await product_service.get_products_by_category_slug(category_slug)


@router.get("/detail/{product_slug}", response_model=ProductSchema)
async def product_detail(product_service: Annotated[ProductService, Depends()], product_slug: str):
    return await product_service.get_product_by_slug(product_slug)


@router.patch("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_service: Annotated[ProductService, Depends()],
    product_id: int,
    product: UpdateProductIn,
    current_user: Annotated[
        UserSchema, Depends(require_roles((UserRole.ADMIN, UserRole.SUPPLIER)))
    ],
):
    return await product_service.update_product(product_id, product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_service: Annotated[ProductService, Depends()],
    product_id: int,
    current_user: Annotated[UserSchema, Depends(require_roles((UserRole.ADMIN,)))],
):
    is_deleted = await product_service.delete_product(product_id)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT if is_deleted else status.HTTP_404_NOT_FOUND
    )


@router.get("/{product_id}/reviews", response_model=list[ReviewSchema], tags=["reviews"])
async def products_reviews(
    product_service: Annotated[ProductService, Depends()],
    review_service: Annotated[ReviewService, Depends()],
    product_id: int,
    current_user: Annotated[UserSchema, Depends(get_current_user)],
):
    product = await product_service.get_product_by_id(product_id)
    return await review_service.get_reviews_by_product_id(product.product_id)


@router.post(
    "/{product_id}/reviews",
    response_model=ReviewSchema,
    tags=["reviews"],
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    product_service: Annotated[ProductService, Depends()],
    review_service: Annotated[ReviewService, Depends()],
    product_id: int,
    review: CreateReviewIn,
    current_user: Annotated[UserSchema, Depends(require_roles((UserRole.CUSTOMER,)))],
):
    product = await product_service.get_product_by_id(product_id)
    return await review_service.create_review(review, current_user.user_id, product.product_id)
