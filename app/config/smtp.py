from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.base import GLOBAL_PATH


class SMTPSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=GLOBAL_PATH, extra="ignore")
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str


settings = SMTPSettings()
