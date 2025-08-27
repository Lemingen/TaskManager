from pydantic import BaseModel

class ResponseTaskModel(BaseModel):
    id: str
    title: str
    description: str
    status: str


class CreateTaskModel(BaseModel):
    title: str
    description: str


class UpdateTaskModel(BaseModel):
    title: str = None
    description: str = None
    status: int = None
