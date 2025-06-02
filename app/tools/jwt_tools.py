from datetime import datetime, timedelta

import jwt

from app.backend import settings
from app.exceptions import InvalidCredentialsError
from app.schemas import UserJWTSchema


def generate_user_jwt_token(user_jwt_schema: UserJWTSchema) -> str:
    payload = {
        "sub": user_jwt_schema.username,
        "user_id": user_jwt_schema.user_id,
        "is_admin": user_jwt_schema.is_admin,
        "is_supplier": user_jwt_schema.is_supplier,
        "is_customer": user_jwt_schema.is_customer,
        "exp": int((datetime.utcnow() + user_jwt_schema.expiration_timeframe).timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def generate_email_confirm_jwt_token(email: str) -> str:
    payload = {
        "sub": email,
        "exp": int((datetime.utcnow() + timedelta(hours=24)).timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_email_confirm_jwt_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        raise InvalidCredentialsError
