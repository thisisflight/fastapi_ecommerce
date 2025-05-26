from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend import get_db
from app.models import Category
from app.schemas import CreateCategoryDB, UpdateCategoryDB


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_categories(self):
        stmt = select(Category)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_category(self, category: CreateCategoryDB) -> Category:
        stmt = (insert(Category)
                .values(**category.model_dump())
                .on_conflict_do_update(index_elements=["slug"], set_={"slug": category.slug})
                .returning(Category))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_category_by_id(self, category_id: int):
        stmt = select(Category).where(Category.category_id == category_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_category_by_slug(self, slug: str):
        stmt = select(Category).where(Category.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def update_category(self, category_id: int, category: UpdateCategoryDB) -> Category | None:
        stmt = (update(Category)
                .where(Category.category_id == category_id)
                .values(**category.model_dump())
                .returning(Category))
        result = await self.session.execute(stmt)
        return result.scalar()

    async def delete_category(self, category_id: int) -> bool:
        stmt = delete(Category).where(Category.category_id == category_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0


async def get_category_repo(session: AsyncSession = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(session)
