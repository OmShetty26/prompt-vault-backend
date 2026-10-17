
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BACKEND_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    secret_key: str = Field(min_length=32)
    database_url: str
    frontend_url: str

    environment: Literal["development", "production"] = "development"
    cookie_samesite: Literal["lax", "none"] = "lax"

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
    )

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()
