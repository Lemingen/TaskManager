import pytest
from pydantic import ValidationError
from app.schemas.task_schemas import ResponseTaskModel, CreateTaskModel, UpdateTaskModel


def test_response_task_model_valid():
    task = ResponseTaskModel(
        id="123",
        title="Test",
        description="Desc",
        status="open"
    )
    assert task.id == "123"
    assert task.status == "open"
    assert task.model_dump()["title"] == "Test"

def test_create_task_model_valid():
    task = CreateTaskModel(title="New Task", description="Do something")
    assert task.title == "New Task"
    assert task.description == "Do something"

def test_create_task_model_missing_field():
    with pytest.raises(ValidationError):
        CreateTaskModel(title="New Task")

def test_update_task_model_partial_update():
    task = UpdateTaskModel(title="Updated")
    assert task.title == "Updated"
    assert task.description is None
    assert task.status is None

def test_update_task_model_invalid_status_type():
    with pytest.raises(ValidationError):
        UpdateTaskModel(status="not_an_int")