import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.fixture(scope="module")
def test_app():
    return app

@pytest.fixture(scope="module")
def client(test_app):
    with TestClient(test_app) as test_client:
        yield test_client

def test_read_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers['content-type']


@pytest.mark.asyncio
async def test_create_paste():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/create", data={"content": "Test Paste", "burn_after_reading": False, "expires_in": 5})