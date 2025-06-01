from typing import Sequence

from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend import get_db
from app.exceptions import ReviewAlreadyExists
from app.models import Product, Review
from app.schemas import CreateReviewDB, DeactivateReviewDB


class ReviewRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get_all_reviews(self) -> Sequence[Review]:
        stmt = select(Review)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_review_by_id(self, review_id: int) -> Review:
        stmt = select(Review).where(Review.review_id == review_id)
        result = await self.session.execute(stmt)
        return result.scalar()

    async def get_reviews_by_product_id(
        self, product_id: int, is_active: bool | None = None
    ) -> Sequence[Review]:
        stmt = select(Review).where(Review.product_id == product_id)
        if is_active is not None:
            stmt = stmt.where(Review.is_active == is_active)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_active_reviews_grades_by_product_id(self, product_id: int) -> Sequence[int]:
        stmt = select(Review.grade).where(
            Review.is_active == True, Review.product_id == product_id  # noqa: E712
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def recalculate_product_rate(self, product_id: int) -> Product:
        reviews_grades = await self.get_active_reviews_grades_by_product_id(product_id=product_id)
        try:
            rating = round(sum(reviews_grades) / len(reviews_grades), 1)
        except ZeroDivisionError:
            rating = 0
        return await self._update_product_rate(product_id=product_id, rating=rating)

    async def _update_product_rate(self, product_id: int, rating: float) -> Product:
        stmt = (
            update(Product)
            .where(Product.product_id == product_id)
            .values(rating=rating)
            .returning(Product)
        )
        result = await self.session.execute(stmt)
        return result.scalar()

    async def create_review(self, review: CreateReviewDB) -> Review:
        try:
            stmt = insert(Review).values(**review.model_dump()).returning(Review)
            result = await self.session.execute(stmt)
            await self.recalculate_product_rate(product_id=review.product_id)
            return result.scalar()
        except IntegrityError as e:
            if "uq_review_user_id_product_id" in str(e):
                raise ReviewAlreadyExists
            raise

    async def deactivate_review(self, review: DeactivateReviewDB) -> Review:
        stmt = (
            update(Review)
            .where(Review.review_id == review.review_id)
            .values(is_active=False)
            .returning(Review)
        )
        result = await self.session.execute(stmt)
        await self.recalculate_product_rate(product_id=review.product_id)
        return result.scalar()


async def get_review_repo(session: AsyncSession = Depends(get_db)) -> ReviewRepository:
    return ReviewRepository(session)
