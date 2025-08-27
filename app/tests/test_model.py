import pytest
from sqlalchemy import select
from app.models.task_model import TaskOrm
from uuid import uuid4
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from app.settings.config import settings
from sqlalchemy.orm import sessionmaker


@pytest.mark.asyncio
async def test_task_orm_crud():
    unique_title = f"Query Test {uuid4()}"
    engine = create_async_engine(settings.get_async_db_url, future=True, echo=True)
    async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session_factory() as session:
        async with session.begin():
            task = TaskOrm(title=unique_title, description="Query desc")
            session.add(task)
            await session.flush()

            result = await session.execute(
                select(TaskOrm).where(TaskOrm.title == unique_title)
            )
            task_from_db = result.scalars().first()
            assert task_from_db is not None
            assert task_from_db.description == "Query desc"
            assert task_from_db.status == "CREATED"

            task_from_db.description = "Updated description"
            await session.flush()

            result = await session.execute(
                select(TaskOrm).where(TaskOrm.id == task_from_db.id)
            )
            updated_task = result.scalars().first()
            assert updated_task.description == "Updated description"

            await session.delete(updated_task)
            await session.flush()

            result = await session.execute(
                select(TaskOrm).where(TaskOrm.id == task_from_db.id)
            )
            deleted_task = result.scalars().first()
            assert deleted_task is None