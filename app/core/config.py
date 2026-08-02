from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)

    PROJECT_NAME: str = "Slate EV Truck API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database
    SQLITE_DB_PATH: Path = Path("app/db/slate.db")

settings = Settings() 