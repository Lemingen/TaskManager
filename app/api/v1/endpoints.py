from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.task_schemas import CreateTaskModel, ResponseTaskModel, UpdateTaskModel
from app.settings.database import get_async_session
from app.view.task_manager_service import TaskManager

app = FastAPI(title="Task Manager API", debug=True)

def get_service(session: AsyncSession = Depends(get_async_session)):
    return TaskManager(session)


@app.post(
    "/tasks/",
    response_model=ResponseTaskModel,
    tags=["Tasks"],
    summary="Создать задачу",
    description="Создаёт новую задачу с заголовком и описанием"
)
async def create_task(
        data: CreateTaskModel,
        task: TaskManager = Depends(get_service)
):
    return await task.create(data.title, data.description)


@app.get(
    "/tasks/{task_id}",
    response_model=ResponseTaskModel,
    tags=["Tasks"],
    summary="Получить задачу",
    description="Возвращает задачу по её идентификатору (UUID)"
)
async def get_task(
        task_id: str,
        task: TaskManager = Depends(get_service)
):
    result = await task.get(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@app.get(
    "/tasks/",
    response_model= list[ResponseTaskModel],
    tags=["Tasks"],
    summary="Получить список задач",
    description="Возвращает список всех задач"
)
async def get_list(
        task: TaskManager = Depends(get_service)
):
    return await task.get_list()


@app.patch(
    "/tasks/{task_id}",
    response_model=ResponseTaskModel,
    tags=["Tasks"],
    summary="Обновить задачу",
    description="Обновляет заголовок, описание или статус задачи по идентификатору задачи"
)
async def update_task(
        task_id: str,
        data: UpdateTaskModel,
        task: TaskManager = Depends(get_service)
):
    result = await task.update(task_id, data.title, data.description, data.status)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Удалить задачу",
    description="Удаляет задачу по её идентификатору"
)
async def delete_task(
        task_id: str,
        task: TaskManager = Depends(get_service)
):
    result = await task.delete(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result