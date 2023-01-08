from pydantic import BaseSettings

class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_database: str
    discounts_api_base: str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()