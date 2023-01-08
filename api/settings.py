from pydantic import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_port: int
    db_host: str
    redis_host: str
    redis_port: int
    discounts_api_base: str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()