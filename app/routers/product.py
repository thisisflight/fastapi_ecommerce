from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.schemas import CreateProductIn, ProductSchema, UpdateProductIn
from app.services import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductSchema])
async def all_products(service: Annotated[ProductService, Depends()]):
    return await service.get_all_products()


@router.post("", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
async def create_product(service: Annotated[ProductService, Depends()], product: CreateProductIn):
    return await service.create_product(product)


@router.get("/{category_slug}", response_model=list[ProductSchema])
async def product_by_category(service: Annotated[ProductService, Depends()], category_slug: str):
    return await service.get_products_by_category_slug(category_slug)


@router.get("/detail/{product_slug}", response_model=ProductSchema)
async def product_detail(service: Annotated[ProductService, Depends()], product_slug: str):
    return await service.get_product_by_slug(product_slug)


@router.patch("/{product_id}", response_model=ProductSchema)
async def update_product(service: Annotated[ProductService, Depends()], product_id: int, product: UpdateProductIn):
    return await service.update_product(product_id, product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(service: Annotated[ProductService, Depends()], product_id: int):
    is_deleted = await service.delete_product(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT if is_deleted else status.HTTP_404_NOT_FOUND)
