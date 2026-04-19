import pytest
from datetime import datetime
from os import environ
from typing import AsyncGenerator

from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Request, Response

from src.__main__ import app
from src.database import Base, App, get_session, DataBase
from src.depends.db import get_db
from src.depends.auth import verify_token
from src.handlers.auth import User
from core.redis_client.dependency import get_redis
from .adt_test_classes import RedisClientMock


engine = create_async_engine(
    url='sqlite+aiosqlite:///:memory:',
    echo=True,
    pool_pre_ping=True,
)
test_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession]:
    async with test_session() as session:
        yield session


@pytest.fixture(scope='session')
async def test_db() -> AsyncGenerator[DataBase]:
    async with test_session() as session:
        yield DataBase(session)


async def get_test_db() -> AsyncGenerator[DataBase]:
    async with test_session() as session:
        yield DataBase(session)


async def verify_test_token(request: Request, response: Response) -> User:
    return User(id=1, name="Test User")


def test_redis_client():
    yield RedisClientMock()


@pytest.fixture(scope='module')
async def test_client() -> AsyncGenerator[AsyncClient]:
    app.dependency_overrides[verify_token] = verify_test_token
    app.dependency_overrides[get_redis] = test_redis_client
    app.dependency_overrides[get_db] = get_test_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
        app.dependency_overrides.clear()


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with test_session() as session:
        db_app = App(
            id=1,
            name='MainTestApp',
            code='test_code_123',
            status_url='-',
            logs_folder='./logs',
            added_by_id=1,
        )
        session.add(db_app)
        await session.commit()
