from fastapi import Depends
from sqlalchemy import delete, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend import get_db
from app.models import Category, Product
from app.schemas import CreateProductDB, UpdateProductDB


class ProductRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get_all_products(self):
        stmt = select(Product).where(Product.is_active == True)  # noqa
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_product(self, product: CreateProductDB):
        stmt = (
            insert(Product)
            .values(**product.model_dump())
            .on_conflict_do_update(index_elements=["slug"], set_={"price": product.price, "stock": product.stock})
            .returning(Product)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_product_by_id(self, product_id: int):
        stmt = select(Product).where(Product.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_product_by_slug(self, slug: str):
        stmt = select(Product).where(Product.slug == slug)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_products_by_category_slug(self, category_slug: str):
        stmt = (
            select(Product)
            .join(Product.category)
            .where(Category.slug == category_slug)
            .where(Product.is_active == True)  # noqa
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_product(self, product_id: int, product: UpdateProductDB):
        stmt = (
            update(Product)
            .where(Product.product_id == product_id)
            .values(**product.model_dump(exclude_unset=True))
            .returning(Product)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def delete_product(self, product_id: int) -> bool:
        stmt = delete(Product).where(Product.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0


async def get_product_repo(session: AsyncSession = Depends(get_db)) -> ProductRepository:
    return ProductRepository(session)
