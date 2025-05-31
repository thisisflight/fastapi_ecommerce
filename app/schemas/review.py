import datetime

from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError

from app.schemas.constants import REVIEW_COMMENT_MAX_LENGTH, REVIEW_COMMENT_MIN_LENGTH


class CreateReviewIn(BaseModel):
    comment: str | None = Field(
        None, min_length=REVIEW_COMMENT_MIN_LENGTH, max_length=REVIEW_COMMENT_MAX_LENGTH
    )
    grade: int

    class Config:
        from_attributes = True

    @field_validator("grade")
    def validate_grade(cls, v: int) -> int:  # noqa
        if not isinstance(v, int):
            raise PydanticCustomError(
                "invalid_grade",
                "Grade must be an integer",
                {"grade": v},
            )
        if v < 1 or v > 5:
            raise PydanticCustomError(
                "invalid_grade",
                "Grade must be between 1 and 5",
                {"grade": v},
            )
        return v

    @field_validator("comment")
    def validate_comment(cls, v: str | None) -> str | None:  # noqa
        if v is None:
            return v
        v = v.strip()
        if len(v) < REVIEW_COMMENT_MIN_LENGTH:
            raise PydanticCustomError(
                "too_short_comment",
                f"Comment must be at least {REVIEW_COMMENT_MIN_LENGTH} characters long",
                {"comment": v},
            )
        if len(v) > REVIEW_COMMENT_MAX_LENGTH:
            raise PydanticCustomError(
                "too_long_comment",
                f"Comment must be at most {REVIEW_COMMENT_MAX_LENGTH} characters long",
                {"comment": v},
            )
        return v


class CreateReviewDB(CreateReviewIn):
    product_id: int
    user_id: int


class DeactivateReviewDB(BaseModel):
    review_id: int
    product_id: int


class ReviewSchema(BaseModel):
    review_id: int
    user_id: int
    product_id: int
    comment: str | None
    created_at: datetime.datetime
    grade: int
    is_active: bool

    class Config:
        from_attributes = True
