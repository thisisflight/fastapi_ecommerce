from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from app.dependency import require_roles
from app.schemas import CategorySchema, CreateCategoryIn, UpdateCategoryIn, UserSchema
from app.services import CategoryService
from app.tools import UserRole

router = APIRouter(prefix="/categories", tags=["category"])


@router.get("", response_model=list[CategorySchema])
async def get_all_categories(service: Annotated[CategoryService, Depends()]):
    return await service.get_all_categories()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CategorySchema)
async def create_category(
    service: Annotated[CategoryService, Depends()],
    category: CreateCategoryIn,
    current_user: Annotated[UserSchema, Depends(require_roles((UserRole.ADMIN,)))],
):
    return await service.create_category(category)


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category_by_id(service: Annotated[CategoryService, Depends()], category_id: int):
    return await service.get_category_by_id(category_id)


@router.get("/slug/{slug}", response_model=CategorySchema)
async def get_category_by_slug(service: Annotated[CategoryService, Depends()], slug: str):
    return await service.get_category_by_slug(slug)


@router.patch("/{category_id}", response_model=CategorySchema)
async def update_category(
    service: Annotated[CategoryService, Depends()],
    category_id: int,
    category: UpdateCategoryIn,
    current_user: Annotated[UserSchema, Depends(require_roles((UserRole.ADMIN,)))],
):
    return await service.update_category(category_id, category)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    service: Annotated[CategoryService, Depends()],
    category_id: int,
    current_user: Annotated[UserSchema, Depends(require_roles((UserRole.ADMIN,)))],
):
    is_deleted: bool = await service.delete_category(category_id)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT if is_deleted else status.HTTP_404_NOT_FOUND
    )
