from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.exceptions import UserAlreadyExists
from app.repos import UserRepository, get_user_repo
from app.schemas import CreateUserDB, CreateUserIn, UserJWTSchema, UserSchema
from app.tools import pwd_context


class UserService:
    def __init__(self, repo: Annotated[UserRepository, Depends(get_user_repo)]):
        self.user_repo = repo

    async def create_user(self, user_schema: CreateUserIn):
        is_user_exists = await self.user_repo.check_if_user_exists(user_schema.username, user_schema.email)
        if not is_user_exists:
            hashed_password = pwd_context.hash(user_schema.password)
            user_data = user_schema.model_dump(exclude={"password"})
            user_db = CreateUserDB(**user_data, hashed_password=hashed_password)
            user = await self.user_repo.create_user(user_db)
            return UserSchema.model_validate(user)
        raise UserAlreadyExists

    async def get_user_by_username(self, username: str):
        user = await self.user_repo.get_user_by_username(username)
        return UserSchema.model_validate(user)

    async def authenticate_user_via_jwt(self, username: str, password: str):
        user = await self.user_repo.get_user_by_username(username)
        if not user or not pwd_context.verify(password, user.hashed_password) or user.is_active == False:  # noqa
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return UserJWTSchema.model_validate(user)
