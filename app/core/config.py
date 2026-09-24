from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "CareReady API"
    environment: Literal["development", "test", "production"] = "development"
    database_url: str = (
        "postgresql+asyncpg://careready:local-development-only@127.0.0.1:5434/careready"
    )
    redis_url: str = "redis://127.0.0.1:6382/0"
