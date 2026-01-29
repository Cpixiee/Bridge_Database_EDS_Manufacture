from pydantic import BaseModel
from functools import lru_cache
import os


class Settings(BaseModel):
    app_name: str = "Cyber Backend API"
    version: str = "1.0.0"

    # Konfigurasi database QA
    db_host: str = "10.62.144.231"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "beny1234"
    db_name: str = "qa"


@lru_cache
def get_settings() -> Settings:
    # Di masa depan bisa dihubungkan ke environment variable (.env)
    return Settings()


