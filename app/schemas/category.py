from pydantic import BaseModel, Field

from app.schemas.constants import CATEGORY_NAME_MAX_LENGTH, CATEGORY_NAME_MIN_LENGTH
from app.schemas.mixins import ValidateCategoryNameMixin


class CreateCategoryIn(ValidateCategoryNameMixin, BaseModel):
    name: str = Field(..., min_length=CATEGORY_NAME_MIN_LENGTH, max_length=CATEGORY_NAME_MAX_LENGTH)
    parent_id: int | None = None


class CreateCategoryDB(CreateCategoryIn):
    slug: str


class UpdateCategoryIn(ValidateCategoryNameMixin, BaseModel):
    name: str = Field(..., min_length=CATEGORY_NAME_MIN_LENGTH, max_length=CATEGORY_NAME_MAX_LENGTH)


class UpdateCategoryDB(UpdateCategoryIn):
    slug: str


class CategorySchema(BaseModel):
    category_id: int
    name: str
    slug: str
    is_active: bool
    parent_id: int | None

    class Config:
        from_attributes = True
