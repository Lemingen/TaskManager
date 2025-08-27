import pytest
from app.api.v1.endpoints import app
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport


@pytest.mark.asyncio
async def test_api_crud():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        create_payload = {"title": "API Task", "description": "API Description"}
        response = await client.post("/tasks/", json=create_payload)
        assert response.status_code == 200
        data = response.json()
        task_id = data["id"]

        response = await client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "API Task"

        response = await client.get("/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert any(task["id"] == task_id for task in data)

        update_payload = {"title": "Updated Title", "description": "Updated Desc", "status": 2}
        response = await client.patch(f"/tasks/{task_id}", json=update_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["description"] == "Updated Desc"
        assert data["status"] == "DONE"

        response = await client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204

        response = await client.get(f"/tasks/{task_id}")
        assert response.status_code == 404
