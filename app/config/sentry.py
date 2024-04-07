from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.base import GLOBAL_PATH


class SentrySettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=GLOBAL_PATH, extra="ignore")
    DSN: str


settings = SentrySettings()
