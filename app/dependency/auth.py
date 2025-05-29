from typing import Annotated

import jwt
from fastapi import Depends

from app.backend import settings
from app.exceptions import InvalidCredentialsError, UserNotFoundError
from app.schemas import UserSchema
from app.services import UserService
from app.tools.oauth2_tools import oauth2_scheme


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], service: Annotated[UserService, Depends()]
) -> UserSchema:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise InvalidCredentialsError("Invalid token payload")

        return await service.get_user_by_username(username)

    except jwt.ExpiredSignatureError:
        raise InvalidCredentialsError("Token expired")
    except (jwt.PyJWTError, UserNotFoundError) as e:
        raise InvalidCredentialsError(str(e))
