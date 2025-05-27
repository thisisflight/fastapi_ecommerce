from typing import Annotated

from fastapi import Depends
from slugify import slugify

from app.repos import ProductRepository, get_product_repo
from app.schemas import CreateProductDB, CreateProductIn, ProductSchema, UpdateProductDB, UpdateProductIn


class ProductService:
    def __init__(self, repo: Annotated[ProductRepository, Depends(get_product_repo)]):
        self.product_repo = repo

    async def create_product(self, product: CreateProductIn):
        slug = slugify(product.name)
        product_db = CreateProductDB(slug=slug, **product.model_dump())
        result = await self.product_repo.create_product(product_db)
        return ProductSchema.model_validate(result)

    async def get_all_products(self):
        products = await self.product_repo.get_all_products()
        return [ProductSchema.model_validate(product) for product in products]

    async def get_product_by_id(self, product_id: int):
        product = await self.product_repo.get_product_by_id(product_id)
        return ProductSchema.model_validate(product)

    async def get_products_by_category_slug(self, category_slug: str):
        products = await self.product_repo.get_products_by_category_slug(category_slug)
        return [ProductSchema.model_validate(product) for product in products]

    async def get_product_by_slug(self, slug: str):
        product = await self.product_repo.get_product_by_slug(slug)
        return ProductSchema.model_validate(product)

    async def update_product(self, product_id: int, product_in: UpdateProductIn):
        existing_product = await self.product_repo.get_product_by_id(product_id)
        if existing_product:
            update_data = product_in.model_dump(exclude_unset=True)
            if "name" in update_data:
                update_data["slug"] = slugify(update_data["name"])
            product_db = UpdateProductDB(**update_data)
            product = await self.product_repo.update_product(product_id, product_db)
            return ProductSchema.model_validate(product)

    async def delete_product(self, product_id: int):
        return await self.product_repo.delete_product(product_id)
