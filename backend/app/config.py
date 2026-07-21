from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "PlanetIQ"
    VERSION: str = "2.0.0"
    DEBUG: bool = True

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./planetiq.db"

    # APIs
    OPEN_METEO_URL: str = "https://api.open-meteo.com/v1/forecast"

    # NASA FIRMS
    FIRMS_API_KEY: str = ""
    FIRMS_URL: str = "https://firms.modaps.eosdis.nasa.gov/api"

    # NDVI (placeholder for future integration)
    NDVI_PROVIDER: str = "sentinel"

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
