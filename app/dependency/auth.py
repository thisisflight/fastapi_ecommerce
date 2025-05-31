from typing import Sequence

import jwt
from fastapi import Depends

from app.backend import settings
from app.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    UserNotFoundError,
    UserPermissionError,
    WrongUsernameCredentialsError,
)
from app.schemas import UserSchema
from app.services import UserService
from app.tools import UserRole
from app.tools.oauth2_tools import oauth2_scheme


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    service: UserService = Depends(),
) -> UserSchema:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise WrongUsernameCredentialsError
        user = await service.get_user_by_username(username)
        if not user.is_active:
            raise InactiveUserError
        return user
    except (jwt.PyJWTError, UserNotFoundError):
        raise InvalidCredentialsError


def require_roles(required_roles: Sequence[UserRole] | None = None):
    async def role_checker(user: UserSchema = Depends(get_current_user)) -> UserSchema:
        if not required_roles:
            return user

        user_roles = []
        if user.is_admin:
            user_roles.append(UserRole.ADMIN)
        if user.is_customer:
            user_roles.append(UserRole.CUSTOMER)
        if user.is_supplier:
            user_roles.append(UserRole.SUPPLIER)

        if not any(role in user_roles for role in required_roles):
            raise UserPermissionError

        return user

    return role_checker
