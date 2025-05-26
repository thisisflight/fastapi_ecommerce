from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str
    ECHO: bool

    class Config:
        case_sensitive = True


settings = Settings()