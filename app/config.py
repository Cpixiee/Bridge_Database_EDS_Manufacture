from functools import lru_cache
import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Bridge Database EDS Manufacture"
    version: str = "1.0.0"

    # Konfigurasi database QA
    db_host: str = os.getenv("DB_HOST", "103.236.140.19")
    db_port: int = int(os.getenv("DB_PORT", "3306"))
    db_user: str = os.getenv("DB_USER", "root")
    db_password: str = os.getenv("DB_PASSWORD", "beny1234")
    db_name: str = os.getenv("DB_NAME", "qa")


@lru_cache
def get_settings() -> Settings:
    return Settings()


