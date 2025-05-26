from pydantic import BaseModel


class CreateCategoryIn(BaseModel):
    name: str
    parent_id: int | None = None


class CreateCategoryDB(CreateCategoryIn):
    slug: str


class UpdateCategoryIn(BaseModel):
    name: str


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
