
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TURSO_DATABASE_URL: str
    TURSO_AUTH_TOKEN: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
