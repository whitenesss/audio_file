from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.conf import db_settings

SQLALCHEMY_DATABASE_URL = (
    "postgresql+asyncpg://"
    f"{db_settings.POSTGRES_USER}:"
    f"{db_settings.POSTGRES_PASSWORD}@"
    f"{db_settings.POSTGRES_HOST}:"
    f"{db_settings.POSTGRES_PORT}/"
    f"{db_settings.POSTGRES_DB}"
)
SQLALCHEMY_DATABASE_URL_ALEMBIC= (
    "postgresql+asyncpg://"
    f"{db_settings.POSTGRES_USER}:"
    f"{db_settings.POSTGRES_PASSWORD}@"
    f"{db_settings.POSTGRES_HOST_ALEMBIC}:"
    f"{db_settings.POSTGRES_PORT}/"
    f"{db_settings.POSTGRES_DB}"
)
async_engine = create_async_engine(
    url=SQLALCHEMY_DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    echo=True,
    pool_pre_ping=True,
    pool_timeout=30,
    pool_recycle=300,
)
async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
        await session.close()


async def get_async_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


