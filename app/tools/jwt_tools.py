from datetime import datetime

import jwt

from app.backend import settings
from app.schemas import UserJWTSchema


def generate_jwt_token(user_jwt_schema: UserJWTSchema) -> str:
    payload = {
        "sub": user_jwt_schema.username,
        "id": user_jwt_schema.user_id,
        "is_admin": user_jwt_schema.is_admin,
        "is_supplier": user_jwt_schema.is_supplier,
        "is_customer": user_jwt_schema.is_customer,
        "exp": int((datetime.utcnow() + user_jwt_schema.expiration_timeframe).timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
