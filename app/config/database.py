from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config.base import GLOBAL_PATH


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=GLOBAL_PATH, env_prefix="DB_", extra="ignore"
    )
    HOST: str
    PORT: int
    USER: str
    PASSWORD: int | str
    NAME: str

    @property
    def get_database_url(self):
        return f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


settings = DBSettings()
engine = create_async_engine(settings.get_database_url)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
