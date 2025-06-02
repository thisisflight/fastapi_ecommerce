from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DOMAIN: str
    DATABASE_URL: str
    ECHO: bool
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_TIME: int
    DEBUG: bool
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    MAIL_SERVER: str
    MAIL_FROM: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SSL_TLS: bool
    MAIL_STARTTLS: bool
    VALIDATE_CERTS: bool

    class Config:
        case_sensitive = True


settings = Settings()


mail_conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_FROM,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS,
)
