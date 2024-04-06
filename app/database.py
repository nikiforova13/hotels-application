import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

src = pathlib.Path(__file__).absolute().parent.joinpath(".env")


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=src)
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: int
    DB_NAME: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str
    SECRET_KEY: str
    APGORITHM: str

    LOG_LEVEL: str

    @property
    def get_database_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = DBSettings()
engine = create_async_engine(settings.get_database_url)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
