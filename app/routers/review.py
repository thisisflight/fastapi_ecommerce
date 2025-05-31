from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependency import require_roles
from app.schemas import ReviewSchema, UserSchema
from app.services import ReviewService
from app.tools import UserRole

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("", response_model=list[ReviewSchema])
async def all_reviews(review_service: Annotated[ReviewService, Depends()]):
    return await review_service.get_all_reviews()


@router.patch("/{review_id}/deactivate", response_model=ReviewSchema)
async def delete_reviews(
    review_service: Annotated[ReviewService, Depends()],
    review_id: int,
    current_user: Annotated[UserSchema, Depends(require_roles((UserRole.ADMIN,)))],
):
    return await review_service.deactivate_review(review_id)
