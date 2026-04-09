import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import DB
from app.database.repo.base import ItemNotFound


async def test_base_app(test_db: AsyncSession):
    apps = await DB.apps.all(session=test_db)
    assert len(apps) == 1
    assert apps[0].name == 'MainTestApp'
    assert apps[0].code == 'test_code_123'


async def test_exists(test_db: AsyncSession):
    ans = await DB.apps.exists(
        app_id=1,
        session=test_db
    )
    assert ans is True


async def test_not_exists(test_db: AsyncSession):
    ans = await DB.apps.exists(
        app_id=100,
        session=test_db
    )
    assert ans is False


async def test_by_id(test_db: AsyncSession):
    app = await DB.apps.by_id(
        app_id=1,
        session=test_db
    )
    assert app is not None
    assert app.name == 'MainTestApp'
    assert app.code == 'test_code_123'
    assert app.added_by_id == 1
    assert app.status_url == '-'
    assert app.logs_folder == './logs'


async def test_by_id_not_existed(test_db: AsyncSession):
    app = await DB.apps.by_id(
        app_id=10,
        session=test_db
    )
    assert app is None


async def test_by_name(test_db: AsyncSession):
    app = await DB.apps.by_name(
        name='MainTestApp',
        session=test_db
    )
    assert app is not None
    assert app.id == 1
    assert app.code == 'test_code_123'
    assert app.added_by_id == 1
    assert app.status_url == '-'
    assert app.logs_folder == './logs'


async def test_by_name_not_existed(test_db: AsyncSession):
    app = await DB.apps.by_name(
        name='MainTestAppOmg_New_not_existed',
        session=test_db
    )
    assert app is None


async def test_by_name_code(test_db: AsyncSession):
    app = await DB.apps.by_name_code(
        name='MainTestApp',
        code='test_code_123',
        session=test_db
    )
    assert app is not None
    assert app.added_by_id == 1
    assert app.status_url == '-'
    assert app.logs_folder == './logs'


async def test_by_name_code_not_existed(test_db: AsyncSession):
    app = await DB.apps.by_name_code(
        name='MainTestApp1235',
        code='test_code_123123545',
        session=test_db
    )
    assert app is None


async def test_codes(test_db: AsyncSession):
    ans = await DB.apps.codes(
        session=test_db
    )
    assert len(ans) == 1
    assert ans[0] == 'test_code_123'


async def test_new(test_db: AsyncSession):
    ans = await DB.apps.new(
        name='NewApp1',
        added_by_id=1,
        status_url='test1',
        logs_folder='test1',
        session=test_db,
    )
    assert ans == True
    assert len(await DB.apps.all(session=test_db)) == 2
    app = await DB.apps.by_name('NewApp1', session=test_db)
    assert app is not None
    assert app.added_by_id == 1
    assert app.status_url == 'test1'
    assert app.logs_folder == 'test1'

    await DB.apps.delete(app, session=test_db)


async def test_new_wrong(test_db: AsyncSession):
    try:
        ans = await DB.apps.new(
            name='MainTestApp',
            added_by_id=0,
            status_url='test1',
            logs_folder='test1',
            session=test_db,
        )
    except Exception as e:
        assert type(e) is IntegrityError


async def test_del_by_id(test_db: AsyncSession):
    app = await DB.apps.by_name('NewApp1', session=test_db)
    assert app is not None

    ans = await DB.apps.del_by_id(app_id=app.id, session=test_db)
    assert ans == True
    assert len(await DB.apps.all(session=test_db)) == 1


async def test_del_by_id_wrong(test_db: AsyncSession):
    try:
        ans = await DB.apps.del_by_id(app_id=12345, session=test_db)
        assert False
    except Exception as e:
        assert type(e) is ItemNotFound