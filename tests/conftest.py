import pytest
from httpx import AsyncClient, ASGITransport
from fastapi.testclient import TestClient
from app.__main__ import app  # Импортируйте ваше FastAPI приложение


@pytest.fixture(scope="module")
async def test_client():
    # Создаем TestClient для тестирования
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest.fixture(scope='module')
def test_db():
    pass