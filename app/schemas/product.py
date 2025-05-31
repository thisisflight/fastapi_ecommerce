from decimal import ROUND_HALF_UP, Decimal

from pydantic import BaseModel, Field, HttpUrl, field_validator
from pydantic_core import PydanticCustomError
from pydantic_core.core_schema import FieldValidationInfo

from app.schemas.constants import (
    PRODUCT_DESCRIPTION_MAX_LENGTH,
    PRODUCT_NAME_MAX_LENGTH,
    PRODUCT_NAME_MIN_LENGTH,
)
from app.schemas.mixins import (
    ValidateNullableProductNameMixin,
    ValidateProductDescriptionMixin,
    ValidateProductNameMixin,
)


class ProductBase(BaseModel):
    price: Decimal = Field(default_factory=lambda: Decimal("0.00"))
    image_url: str | None = None
    stock: int = 0

    @field_validator("price", mode="before")
    def validate_price(cls, v, info: FieldValidationInfo) -> Decimal:  # noqa
        if v is None:
            return v if isinstance(cls, UpdateProductIn) else Decimal("0.00")

        if isinstance(v, Decimal):
            return v.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

        if isinstance(v, bool) or not isinstance(v, (str, float, int)):
            raise PydanticCustomError(
                "invalid_price",
                "Price must be a number",
                {"price": v},
            )

        value = (
            Decimal(str(v)).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
            if isinstance(v, (str, float, int))
            else v
        )

        if value < 0:
            raise PydanticCustomError(
                "negative_price",
                "Price cannot be negative",
                {"price": value},
            )
        return value

    @field_validator("stock")
    def validate_stock(cls, v: int | None) -> int:  # noqa
        if v is None and isinstance(cls, UpdateProductIn):
            return v
        if v is None and isinstance(cls, CreateProductIn):
            return 0
        if v < 0:
            raise PydanticCustomError(
                "negative_stock",
                "Stock cannot be negative",
                {"stock": v},
            )
        return v

    @field_validator("image_url")
    def validate_image_url(cls, v: str | None) -> str | None:  # noqa
        if v is not None:
            return str(HttpUrl(v))
        return v


class CreateProductIn(ValidateProductNameMixin, ValidateProductDescriptionMixin, ProductBase):
    name: str = Field(..., min_length=PRODUCT_NAME_MIN_LENGTH, max_length=PRODUCT_NAME_MAX_LENGTH)
    description: str | None = Field(None, max_length=PRODUCT_DESCRIPTION_MAX_LENGTH)
    category_id: int

    class Config:
        from_attributes = True


class CreateProductDB(CreateProductIn):
    slug: str
    supplier_id: int


class UpdateProductIn(
    ValidateNullableProductNameMixin, ValidateProductDescriptionMixin, ProductBase
):
    name: str | None = Field(
        None, min_length=PRODUCT_NAME_MIN_LENGTH, max_length=PRODUCT_NAME_MAX_LENGTH
    )
    description: str | None = Field(None, max_length=PRODUCT_DESCRIPTION_MAX_LENGTH)
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
    image_url: str | None = None
    stock: int
    rating: float
    is_active: bool
    category_id: int
    supplier_id: int

    class Config:
        from_attributes = True
