from decimal import Decimal

from pydantic import BaseModel


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
    supplier_id: int


class UpdateProductIn(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    image_url: str | None = None
    stock: int | None = None
    category_id: int | None = None
    supplier_id: int | None = None


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
    supplier_id: int

    class Config:
        from_attributes = True
