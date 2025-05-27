from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.exceptions import UserAlreadyExists
from app.schemas import CreateUserIn
from app.services import UserService
from app.tools import generate_jwt_token

router = APIRouter(prefix="", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(service: Annotated[UserService, Depends()], user: CreateUserIn):
    try:
        return await service.create_user(user)
    except UserAlreadyExists:
        return Response(status_code=status.HTTP_409_CONFLICT)


@router.post("/token")
async def login(service: Annotated[UserService, Depends()], form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_jwt_schema = await service.authenticate_user_via_jwt(form_data.username, form_data.password)
    token = generate_jwt_token(user_jwt_schema)
    return {"access_token": token, "token_type": "bearer"}
