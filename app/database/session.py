from sqlalchemy.ext.asyncio import AsyncSession

from core.debug import create_log
from .database import new_session


async def get_session():
    async with new_session() as session:
        yield session


def connect_session(method):
    async def wrapper(*args, **kwargs):
        async with new_session() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                create_log(e, 'crit')
                await session.rollback()
                raise e
    return wrapper