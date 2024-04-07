from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.base import GLOBAL_PATH


class SMTPSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=GLOBAL_PATH, extra="ignore")
    SECRET_KEY: str
    APGORITHM: str


settings = SMTPSettings()
