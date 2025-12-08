import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.__main__ import app
from app.database import Base, get_session, App, User, DB
from app.core.auth import get_hash, verify_token, TokenData
from app.depends import TokenDep, SessionDep


engine = create_async_engine(
    url="sqlite+aiosqlite:///dispatcher_test.sqlite3",
    echo=True,
    pool_pre_ping=True,
)
test_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession]:
    print('!!!!!!!!!!!!!!!!!!!!!!!!! test !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    async with test_session() as session:
        yield session


async def verify_test_token() -> TokenData:
    session = get_test_session()
    user = await DB.users.by_id(1, session=session)
    return TokenData(
        user=user,
        exp=10
    )


@pytest.fixture(scope='session')
async def test_client() -> AsyncGenerator[AsyncClient]:
    print('???????????????????????????????? TEST ???????????????????????????')
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        app.dependency_overrides[get_session] = get_test_session
        app.dependency_overrides[SessionDep] = get_test_session
        app.dependency_overrides[verify_token] = verify_test_token
        app.dependency_overrides[TokenDep] = verify_test_token

        print('>>>>>>>>>>>>>>>>>>>', app.dependency_overrides.items())
        yield client
        app.dependency_overrides.clear()


@pytest.fixture(scope='function')
async def test_db() -> AsyncGenerator[AsyncSession]:
    async with test_session() as session:
        yield session


@pytest.fixture(scope='session', autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    #async with test_session() as session:
    #    user = User(id=1, name='test', password=get_hash('123456'))
    #    session.add(user)
    #    await session.flush()
    #    db_app = App(
    #        id=1,
    #        name='MainTestApp',
    #        code='test_code_123',
    #        status_url='-',
    #        logs_folder='-',
    #        added_by_id=user.id,
    #    )
    #    session.add(db_app)
    #    await session.commit()
