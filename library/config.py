"""FastAPI configuration variables."""
from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

library_path = os.path.dirname(os.path.abspath(__file__))
class settingsModel(BaseSettings):
    ENV_TYPE: str = "temp"
    UPLOAD_FOLDER: str =  os.path.join(library_path ,'static/uploads/')
    STORAGE_FOLDER: str = os.path.join(library_path ,'static/storage/')
    MODEL_FOLDER: str = os.path.join(library_path ,'models/')
    ALLOWED_IMAGE_EXTENSIONS: Any = ['PNG', 'JPG', 'JPEG', 'GIF', 'WEBP']
    CACHE_TIMEOUT_PERIOD: int = 900
    OAUTH_SCHEME: Any = "temp"

    model_config = SettingsConfigDict(
        env_file=(
            ".env.production.local",
            ".env.development.local"
            ".env",
        )
    )

Settings = settingsModel()
