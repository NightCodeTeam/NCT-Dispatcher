import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import DB


async def test_base_app(test_db: AsyncSession):
    apps = await DB.apps.all(session=test_db)
    assert len(apps) == 1
    assert apps[0].name == 'MainTestApp'
    assert apps[0].code == 'test_code_123'
