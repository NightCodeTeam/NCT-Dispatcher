from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.debug import logger
from .database import new_session


async def get_session() -> AsyncGenerator[AsyncSession]:
    try:
        async with new_session() as session:
            yield session
    except Exception as e:
        logger.log(e, 'crit')
        await session.rollback()
        raise e
