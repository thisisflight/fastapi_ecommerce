from typing import Annotated

from fastapi import Depends

from app.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
    UserAlreadyExists,
    UserNotFoundError,
)
from app.repos import UserRepository, get_user_repo
from app.schemas import CreateUserDB, CreateUserIn, UserJWTSchema, UserSchema
from app.tools import pwd_context
from app.tools.jwt_tools import decode_email_confirm_jwt_token, generate_email_confirm_jwt_token
from app.workers import send_verification_email


class UserService:
    def __init__(self, repo: Annotated[UserRepository, Depends(get_user_repo)]):
        self.user_repo = repo

    async def create_user(self, user_schema: CreateUserIn):
        is_user_exists = await self.user_repo.check_if_user_exists(
            user_schema.username, user_schema.email
        )
        if not is_user_exists:
            hashed_password = pwd_context.hash(user_schema.password)
            user_data = user_schema.model_dump(exclude={"password"})
            user_db = CreateUserDB(**user_data, hashed_password=hashed_password)
            user = await self.user_repo.create_user(user_db)
            email_verify_token = generate_email_confirm_jwt_token(user.email)
            send_verification_email.delay(email=user.email, token=email_verify_token)
            return UserSchema.model_validate(user)
        raise UserAlreadyExists

    async def verify_email(self, email_verify_token: str):
        email = decode_email_confirm_jwt_token(email_verify_token)
        user_to_activate = await self.user_repo.get_user_by_email(email)
        if user_to_activate:
            user = await self.user_repo.activate_user(email)
            return UserSchema.model_validate(user)
        raise UserNotFoundError

    async def get_user_by_username(self, username: str):
        user = await self.user_repo.get_user_by_username(username)
        return UserSchema.model_validate(user)

    async def authenticate_user_via_jwt(self, username: str, password: str):
        user = await self.user_repo.get_user_by_username(username)
        if not user or not pwd_context.verify(password, user.hashed_password):
            raise InvalidCredentialsError
        if not user.is_active:
            raise InactiveUserError
        return UserJWTSchema.model_validate(user)
