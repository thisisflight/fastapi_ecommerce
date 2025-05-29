from datetime import timedelta

from pydantic import BaseModel, EmailStr

from app.backend import settings


class CreateUserIn(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str


class CreateUserDB(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    is_supplier: bool
    is_customer: bool

    class Config:
        from_attributes = True


class UserJWTSchema(BaseModel):
    username: str
    user_id: int
    is_admin: bool
    is_supplier: bool
    is_customer: bool
    expiration_timeframe: timedelta = timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_TIME)

    class Config:
        from_attributes = True
