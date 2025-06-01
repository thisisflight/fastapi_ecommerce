from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    ECHO: bool
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_TIME: int
    DEBUG: bool

    class Config:
        case_sensitive = True


settings = Settings()
