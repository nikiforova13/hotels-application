from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.base import GLOBAL_PATH


class CelerySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=GLOBAL_PATH, env_prefix="CELERY_", extra="ignore"
    )
    BROKER: str


settings = CelerySettings()
