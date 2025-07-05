from os import getenv
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = "localhost"
    database_port: str = "5432"
    database_username: str = "postgres"
    database_password: str = "password"
    database_name: str = "mydatabase"
    secret_key: str = "your_default_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str = "DATABASE_URL" 
    class Config:
        env_file = ".env"

settings = Settings()
