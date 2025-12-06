import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from fastapi.testclient import TestClient

from app.core.debug import create_log
from app.database.database import Base
from app.database.models import App, Incident
from app.__main__ import app  # Импортируйте ваше FastAPI приложение


@pytest_asyncio.fixture(scope="module")
async def test_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(scope='module')
async def test_db():
    engine = create_async_engine("sqlite+aiosqlite:///dispatcher.sqlite3")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    test_session = async_sessionmaker(engine, expire_on_commit=False)

    async with test_session() as session:
        yield session
        await session.rollback()