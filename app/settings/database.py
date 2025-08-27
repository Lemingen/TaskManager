from typing import Any, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.settings.config import settings
from sqlalchemy.orm import DeclarativeBase

async_engine = create_async_engine(
    settings.get_async_db_url,
    echo = True
)

async_session_factory = async_sessionmaker(
    bind = async_engine,
    class_= AsyncSession
)

async def get_async_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with async_session_factory() as session:
        yield session

class Base(DeclarativeBase):
    ...