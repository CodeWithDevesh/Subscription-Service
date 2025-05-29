import pytest_asyncio
from httpx import AsyncClient
from app.main import app

@pytest_asyncio.fixture
async def client():
    """
    Fixture to provide an asynchronous test client for FastAPI.
    """
    async with AsyncClient(base_url="http://localhost:8000/") as c:
        yield c

@pytest_asyncio.fixture
async def user_token(client):
    res = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "test1234"
    })
    assert res.status_code == 200
    return res.json()["data"]["access_token"]

@pytest_asyncio.fixture
async def admin_token(client):
    res = await client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "test1234"
    })
    assert res.status_code == 200
    return res.json()["data"]["access_token"]