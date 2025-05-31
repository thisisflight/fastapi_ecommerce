from pydantic import ConfigDict, field_validator
from pydantic_core import PydanticCustomError

from app.schemas.constants import (
    CATEGORY_NAME_MIN_LENGTH,
    PRODUCT_DESCRIPTION_MAX_LENGTH,
    PRODUCT_NAME_MIN_LENGTH,
)


class ValidateNotNullStringMixin:
    _model_name: str
    _min_length: int
    _trim_whitespace: bool = True
    _field_name: str = "name"

    model_config = ConfigDict(extra="ignore")

    def __init_subclass__(cls, **kwargs):

        validator_name = f"validate_{cls._field_name}"

        @field_validator(cls._field_name)
        def validate_field(cls, value: str):  # noqa
            if cls._trim_whitespace:
                value = value.strip()

            if not value:
                raise PydanticCustomError(
                    f"empty_{cls._model_name}_name",
                    f"{cls._model_name.capitalize()} name cannot be empty",
                    {},
                )

            if len(value) < cls._min_length:
                raise PydanticCustomError(
                    "too_short_name",
                    f"{cls._model_name.capitalize()} name must be at least {cls._min_length} "
                    f"characters long (after trimming spaces)",
                    {"min_length": cls._min_length, "actual_length": len(value)},
                )

            return value

        setattr(cls, validator_name, validate_field)


class ValidateNullableStringMixin:
    _model_name: str
    _max_length: int = 2000
    _trim_whitespace: bool = True
    _field_name: str = "name"

    model_config = ConfigDict(extra="ignore")

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        validator_name = f"validate_{cls._field_name}"

        @field_validator(cls._field_name)
        def validate_field(cls, value: str | None):
            if value is None:
                return value

            if cls._trim_whitespace:
                value = value.strip()

            if len(value) > cls._max_length:
                raise PydanticCustomError(
                    f"too_long_{cls._field_name}",
                    f"{cls._model_name.capitalize()} {cls._field_name} must be at most {cls._max_length} "
                    f"characters long (after trimming spaces)",
                    {"max_length": cls._max_length, "actual_length": len(value)},
                )

            return value

        setattr(cls, validator_name, validate_field)


class ValidateCategoryNameMixin(ValidateNotNullStringMixin):
    _model_name = "category"
    _min_length = CATEGORY_NAME_MIN_LENGTH


class ValidateProductNameMixin(ValidateNotNullStringMixin):
    _model_name = "product"
    _min_length = PRODUCT_NAME_MIN_LENGTH


class ValidateNullableProductNameMixin(ValidateProductNameMixin):
    pass


class ValidateProductDescriptionMixin(ValidateNullableStringMixin):
    _model_name = "product"
    _max_length = PRODUCT_DESCRIPTION_MAX_LENGTH
    _field_name = "description"
