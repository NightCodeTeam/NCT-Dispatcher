import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import DB
from app.core.auth import verify_hashed


async def test_base_user(test_db: AsyncSession):
    users = await DB.users.all(session=test_db)
    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].name == 'test'
    assert verify_hashed('123456', users[0].password)


async def test_exists(test_db: AsyncSession):
    ans = await DB.users.exists(
        username='test',
        session=test_db
    )
    assert ans is True


async def test_by_id(test_db: AsyncSession):
    user = await DB.users.by_id(
        user_id=1,
        session=test_db
    )
    assert user is not None
    assert user.name == 'test'
    assert verify_hashed('123456', user.password)


async def test_by_name(test_db: AsyncSession):
    user = await DB.users.by_name(
        name='test',
        session=test_db
    )
    assert user is not None
    assert user.id == 1
    assert verify_hashed('123456', user.password)


async def test_new(test_db: AsyncSession):
    ans = await DB.users.new(
        username='NewUser',
        password='test_password',
        session=test_db,
    )
    assert ans == True
    assert len(await DB.users.all(session=test_db)) == 2

    user = await DB.users.by_name('NewUser', session=test_db)
    assert user is not None
