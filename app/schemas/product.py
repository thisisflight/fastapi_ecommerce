from pydantic import BaseModel
from decimal import Decimal


class CreateProductIn(BaseModel):
    name: str
    description: str
    price: Decimal | None = None
    image_url: str
    stock: int | None = None
    category_id: int | None = None

    class Config:
        from_attributes = True


class CreateProductDB(CreateProductIn):
    slug: str


class UpdateProductIn(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    image_url: str | None = None
    stock: int | None = None
    category_id: int | None = None


class UpdateProductDB(UpdateProductIn):
    slug: str | None = None


class ProductSchema(BaseModel):
    product_id: int
    name: str
    slug: str
    description: str | None = None
    price: Decimal
    image_url: str
    stock: int
    rating: float
    is_active: bool
    category_id: int

    class Config:
        from_attributes = True
