from pydantic import BaseModel
from functools import lru_cache
import os


class Settings(BaseModel):
    app_name: str = "Cyber Backend API"
    version: str = "1.0.0"

    db_host: str = "103.236.140.19"
    db_port: int = 3306
    db_user: str = "root"
    db_password: str = "cyber"
    db_name: str = "cyber"


@lru_cache
def get_settings() -> Settings:
    # Di masa depan bisa dihubungkan ke environment variable (.env)
    return Settings()


