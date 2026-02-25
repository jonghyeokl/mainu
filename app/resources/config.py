from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ACCESS_TOKEN_SECRET_KEY: str = "welcome to mainu project!"
    ALGORITHM: str = "HS256"


conf = Settings()
