from typing import Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend import get_db
from app.models import Review


class ReviewRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get_all_reviews(self) -> Sequence[Review]:
        stmt = select(Review)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_reviews_by_product_id(self, product_id: int) -> Sequence[Review]:
        stmt = select(Review).where(Review.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


async def get_review_repo(session: AsyncSession = Depends(get_db)) -> ReviewRepository:
    return ReviewRepository(session)
