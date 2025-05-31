from fastapi import Depends

from app.exceptions import ReviewNotFoundError
from app.repos import ReviewRepository, get_review_repo
from app.schemas import CreateReviewDB, CreateReviewIn, DeactivateReviewDB, ReviewSchema


class ReviewService:
    def __init__(self, review_repo: ReviewRepository = Depends(get_review_repo)):
        self.review_repo = review_repo

    async def get_all_reviews(self):
        return await self.review_repo.get_all_reviews()

    async def get_review_by_id(self, review_id: int):
        review = await self.review_repo.get_review_by_id(review_id)
        if review:
            return ReviewSchema.model_validate(review)
        raise ReviewNotFoundError

    async def get_reviews_by_product_id(self, product_id: int) -> list[ReviewSchema]:
        return await self.review_repo.get_reviews_by_product_id(product_id)

    async def create_review(
        self, review: CreateReviewIn, user_id: int, product_id: int
    ) -> ReviewSchema:
        review_db = CreateReviewDB(user_id=user_id, product_id=product_id, **review.model_dump())
        result = await self.review_repo.create_review(review_db)
        return ReviewSchema.model_validate(result)

    async def deactivate_review(self, review_id: int) -> ReviewSchema:
        review = await self.get_review_by_id(review_id)
        if review:
            review_db = DeactivateReviewDB(**review.model_dump())
            result = await self.review_repo.deactivate_review(review_db)
            return ReviewSchema.model_validate(result)
        raise ReviewNotFoundError
