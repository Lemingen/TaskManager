from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from app.models.task_model import TaskOrm

class TaskManager:
    def __init__(self, session: AsyncSession):
        """
        Сервис для управления задачами.

        Args:
            session (AsyncSession): Асинхронная сессия SQLAlchemy.
        """
        self.session = session
        self.statuses = {
            0: "CREATED",
            1: "IN PROCESS",
            2: "DONE"
        }

    async def create(self, title: str, description: str) -> TaskOrm:
        """
        Создать новую задачу.

        Args:
            title (str): Заголовок задачи.
            description (str): Описание задачи.

        Returns:
            TaskOrm: Созданная задача.
        """
        task = TaskOrm(
            title=title,
            description=description
        )
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get(self, task_id: str) -> TaskOrm | None:
        """
        Получить задачу по её ID.

        Args:
            task_id (str): UUID задачи.

        Returns:
            TaskOrm | None: Объект задачи, если найден, иначе None.
        """
        query = select(TaskOrm).where(TaskOrm.id == task_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_list(self) -> list[TaskOrm]:
        """
        Получить список всех задач.

        Returns:
            list[TaskOrm]: Список объектов задач.
        """
        query = select(TaskOrm)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(
            self,
            task_id: str,
            title: str = None,
            description: str = None,
            status: int = None
            )-> TaskOrm | None:
        """
        Обновить задачу по её ID.

        Args:
            task_id (str): UUID задачи.
            title (str, optional): Новый заголовок задачи.
            description (str, optional): Новое описание задачи.
            status (int, optional): Новый статус задачи (0 - CREATED, 1 - IN PROCESS, 2 - DONE).

        Returns:
            TaskOrm | None: Обновлённая задача, если найдена, иначе None.
        """
        query = select(TaskOrm).where(TaskOrm.id == task_id)
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if task:
            if title:
                task.title = title
            if description:
                task.description = description
            if status is not None:
                task.status = self.statuses.get(status)
            await self.session.commit()
            await self.session.refresh(task)
        return task


    async def delete(self, task_id: str) -> bool:
        """
        Удалить задачу по её ID.

        Args:
            task_id (str): UUID задачи.

        Returns:
            bool: True, если задача была удалена, False, если задача не найдена.
        """
        query = select(TaskOrm).where(TaskOrm.id == task_id)
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True
