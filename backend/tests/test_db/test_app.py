import pytest
from sqlalchemy.exc import IntegrityError

from src.database import DataBase, App
from core.sql_repository.exeptions import ItemNotFound


async def test_base_app(test_db: DataBase):
    await test_db.apps.clear_table()
    db_app = App(
        id=1,
        name='MainTestApp',
        code='test_code_123',
        status_url='-',
        logs_folder='./logs',
        added_by_id=1,
    )
    test_db.session.add(db_app)
    await test_db.session.commit()

    apps = await test_db.apps.all()
    assert len(apps) == 1
    assert apps[0].name == 'MainTestApp'
    assert apps[0].code == 'test_code_123'


async def test_exists(test_db: DataBase):
    ans = await test_db.apps.exists(app_id=1)
    assert ans is True


async def test_not_exists(test_db: DataBase):
    ans = await test_db.apps.exists(app_id=100)
    assert ans is False


async def test_by_id(test_db: DataBase):
    app = await test_db.apps.by_id(app_id=1)
    assert app is not None
    assert app.name == 'MainTestApp'
    assert app.code == 'test_code_123'
    assert app.added_by_id == 1
    assert app.status_url == '-'
    assert app.logs_folder == './logs'


async def test_by_id_not_existed(test_db: DataBase):
    app = await test_db.apps.by_id(app_id=10)
    assert app is None


async def test_by_name(test_db: DataBase):
    app = await test_db.apps.by_name(name='MainTestApp')
    assert app is not None
    assert app.id == 1
    assert app.code == 'test_code_123'
    assert app.added_by_id == 1
    assert app.status_url == '-'
    assert app.logs_folder == './logs'


async def test_by_name_not_existed(test_db: DataBase):
    app = await test_db.apps.by_name(
        name='MainTestAppOmg_New_not_existed'
    )
    assert app is None


async def test_by_name_code(test_db: DataBase):
    app = await test_db.apps.by_name_code(
        name='MainTestApp',
        code='test_code_123'
    )
    assert app is not None
    assert app.added_by_id == 1
    assert app.status_url == '-'
    assert app.logs_folder == './logs'


async def test_by_name_code_not_existed(test_db: DataBase):
    app = await test_db.apps.by_name_code(
        name='MainTestApp1235',
        code='test_code_123123545'
    )
    assert app is None


async def test_codes(test_db: DataBase):
    ans = await test_db.apps.codes()
    assert len(ans) == 1
    assert ans[0] == 'test_code_123'


async def test_new(test_db: DataBase):
    ans = await test_db.apps.new(
        name='NewApp1',
        added_by_id=1,
        status_url='test1',
        logs_folder='test1',
    )
    assert ans == True
    assert len(await test_db.apps.all()) == 2
    app = await test_db.apps.by_name('NewApp1')
    assert app is not None
    assert app.added_by_id == 1
    assert app.status_url == 'test1'
    assert app.logs_folder == 'test1'

    await test_db.apps.delete(app)


async def test_new_wrong(test_db: DataBase):
    try:
        ans = await test_db.apps.new(
            name='MainTestApp',
            added_by_id=0,
            status_url='test1',
            logs_folder='test1',
            commit=True
        )
    except IntegrityError:
        await test_db.session.rollback()
        assert True
        assert len(await test_db.apps.all()) == 1


async def test_del_by_id(test_db: DataBase):
    ans = await test_db.apps.del_by_id(app_id=1)
    assert ans == True
    assert len(await test_db.apps.all()) == 0
    await test_db.session.rollback()


async def test_del_by_id_wrong(test_db: DataBase):
    try:
        ans = await test_db.apps.del_by_id(app_id=12345)
        assert False
    except ItemNotFound:
        assert True
