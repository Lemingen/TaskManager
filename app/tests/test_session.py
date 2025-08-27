import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.settings.config import settings
from app.settings.database import get_async_session, async_engine, async_session_factory
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


@pytest.mark.asyncio
async def test_async_engine_url():
    assert "postgresql+asyncpg://" in str(async_engine.url)

@pytest.mark.asyncio
async def test_async_session_factory_creates_session():
    async with async_session_factory() as session:
        assert isinstance(session, AsyncSession)

@pytest.mark.asyncio
async def test_get_async_session_yields_session():
    gen = get_async_session()
    session = await gen.__anext__()
    assert isinstance(session, AsyncSession)
    await gen.aclose()

@pytest.mark.asyncio
async def test_get_async_session_yields_session_and_executes_query():
    engine = create_async_engine(settings.get_async_db_url, echo=True)
    session_factory = async_sessionmaker(bind=engine)
    async with session_factory() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar_one()
        assert value == 1


