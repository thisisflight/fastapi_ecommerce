from typing import Annotated

import jwt
from fastapi import Depends

from app.backend import settings
from app.exceptions import InvalidCredentialsError, UserNotFoundError, UserPermissionError
from app.schemas import UserSchema
from app.services import UserService
from app.tools import UserRole
from app.tools.oauth2_tools import oauth2_scheme


def role_checker(required_roles: list[UserRole] | None = None) -> Annotated[UserSchema, Depends()]:
    async def role_checker_wrapper(
        token: str = Depends(oauth2_scheme),
        service: UserService = Depends(),
    ) -> UserSchema:
        return await get_current_user(token, service, required_roles)

    return role_checker_wrapper


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[UserService, Depends()],
    required_roles: list[UserRole] | None = None,
) -> UserSchema:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise InvalidCredentialsError("Invalid token payload")

        user_schema = await service.get_user_by_username(username)
        if required_roles and not check_user_role(user_schema, required_roles):
            raise UserPermissionError
        return user_schema

    except jwt.ExpiredSignatureError:
        raise InvalidCredentialsError("Token expired")
    except (jwt.PyJWTError, UserNotFoundError) as e:
        raise InvalidCredentialsError(str(e))


def check_user_role(user: UserSchema, required_roles: list[UserRole] | None = None) -> bool:
    if not required_roles:
        return True
    user_roles = []
    if user.is_admin:
        user_roles.append(UserRole.ADMIN)
    if user.is_customer:
        user_roles.append(UserRole.CUSTOMER)
    if user.is_supplier:
        user_roles.append(UserRole.SUPPLIER)
    return any(role in user_roles for role in required_roles)
