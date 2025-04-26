from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    API_PREFIX: str = "/api"
    CORS_ORIGINS: list[str] = ["*"]  # tighten in prod
    SQL_ECHO: bool = False

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:  # handy for DI
    return Settings()

settings = get_settings()
