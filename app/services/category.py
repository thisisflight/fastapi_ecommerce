from typing import Annotated

from fastapi import Depends
from slugify import slugify

from app.exceptions import CategoryNotFoundError
from app.repos import CategoryRepository, get_category_repo
from app.schemas import (
    CategorySchema,
    CreateCategoryDB,
    CreateCategoryIn,
    UpdateCategoryDB,
    UpdateCategoryIn,
)


class CategoryService:
    def __init__(self, repo: Annotated[CategoryRepository, Depends(get_category_repo)]):
        self.category_repo = repo

    async def create_category(self, category: CreateCategoryIn) -> CategorySchema | None:
        slug = slugify(category.name)
        category_db = CreateCategoryDB(slug=slug, **category.model_dump())
        result = await self.category_repo.create_category(category_db)
        return CategorySchema.model_validate(result)

    async def get_all_categories(self) -> list[CategorySchema]:
        categories = await self.category_repo.get_all_categories()
        return [CategorySchema.model_validate(category) for category in categories]

    async def get_category_by_id(self, category_id: int) -> CategorySchema | None:
        category = await self.category_repo.get_category_by_id(category_id)
        if category:
            return CategorySchema.model_validate(category)
        raise CategoryNotFoundError

    async def get_category_by_slug(self, slug: str) -> CategorySchema | None:
        category = await self.category_repo.get_category_by_slug(slug)
        if category:
            return CategorySchema.model_validate(category)
        raise CategoryNotFoundError

    async def update_category(
        self, category_id: int, category_in: UpdateCategoryIn
    ) -> CategorySchema | None:
        existing_category = await self.category_repo.get_category_by_id(category_id)
        if existing_category:
            slug = slugify(category_in.name)
            category_db = UpdateCategoryDB(slug=slug, **category_in.model_dump())
            category = await self.category_repo.update_category(category_id, category_db)
            return CategorySchema.model_validate(category)
        raise CategoryNotFoundError

    async def delete_category(self, category_id: int) -> bool:
        return await self.category_repo.delete_category(category_id)
