from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_uri: str = "postgresql://postgres:password@db:5432/log-db"

settings = Settings()