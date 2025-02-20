from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str = "mysql://user:password@localhost/dbname"
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CACHE_EXPIRE_MINUTES: int = 5

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings() 