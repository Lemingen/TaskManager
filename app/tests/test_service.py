import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.view.task_manager_service import TaskManager
from app.settings.config import settings


@pytest.mark.asyncio
async def test_task_manager_crud():
    engine = create_async_engine(settings.get_async_db_url, future=True, echo=True)
    async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_factory() as session:
        manager = TaskManager(session)

        task = await manager.create(title="Test Task", description="Test Description")
        assert task.id is not None
        assert task.title == "Test Task"
        assert task.description == "Test Description"

        fetched = await manager.get(task.id)
        assert fetched is not None
        assert fetched.title == task.title

        updated = await manager.update(task.id, title="Updated Title", description="Updated Desc")
        assert updated.title == "Updated Title"
        assert updated.description == "Updated Desc"

        deleted = await manager.delete(task.id)
        assert deleted is True

    await engine.dispose()
