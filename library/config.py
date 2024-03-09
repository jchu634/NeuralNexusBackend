"""FastAPI configuration variables."""
from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

library_path = os.path.dirname(os.path.abspath(__file__))


class settingsModel(BaseSettings):
    ENV_TYPE: str = "temp"
    UPLOAD_FOLDER: str = os.path.join(library_path, 'static/uploads/')
    STORAGE_FOLDER: str = os.path.join(library_path, 'static/storage/')
    MODEL_FOLDER: str = os.path.join(library_path, 'models/')
    ALLOWED_IMAGE_EXTENSIONS: Any = ['PNG', 'JPG', 'JPEG', 'GIF', 'WEBP']
    IMAGE_DEFAULT_EXPIRY_PERIOD: int = 2592000
    CACHE_TIMEOUT_PERIOD: int = 900

    OAUTH_SCHEME: Any = "temp"
    AUTH_SECRET_KEY: str = "blank"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    AUTH_ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(
        env_file=(
            ".env.production.local",
            ".env.development.local"
            ".env",
        )
    )


Settings = settingsModel()
