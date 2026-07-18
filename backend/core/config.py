from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    OPEN_METEO_URL: str = "https://api.open-meteo.com/v1/forecast"
    FIRMS_API_KEY: str = ""
    FIRMS_URL: str = "https://firms.modaps.eosdis.nasa.gov/api"
    DATABASE_URL: str = "sqlite:///./planetiq.db"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
