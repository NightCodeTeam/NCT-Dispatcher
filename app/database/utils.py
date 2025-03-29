from typing import Union
from sqlalchemy import text, select, MetaData
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Incident, App, BannedIP
from app.database.database import Base
from .session import new_session


Tables = Union[App, Incident, BannedIP]

async def get_object_from_db(
    table: Tables,
    filter: str | None = None,
    limit: int | None = None,
    session: AsyncSession | None = None
) -> tuple[Base]: #List[Dict[str, Any]]:
    if filter is not None:
        query = select(table).filter(text(filter))
    else:
        query = select(table)
    if limit:
        query = query.limit(limit)

    if session is None:
        async with new_session() as ss:
            result = await ss.execute(query)
    else:
        result = await session.execute(query)
    return tuple(result.scalars().all())


async def get_apps_from_db(
    filter: str | None = None,
    limit: int | None = None,
    session: AsyncSession | None = None
) -> tuple[App]:
    return await get_object_from_db(App, filter=filter, limit=limit, session=session)


async def get_incidents_from_db(
    filter: str | None = None,
    limit: int | None = None,
    session: AsyncSession | None = None
) -> tuple[Incident]:
    return await get_object_from_db(Incident, filter=filter, limit=limit, session=session)


async def get_banned_ips_from_db(
    filter: str | None = None,
    limit: int | None = None,
    session: AsyncSession | None = None
) -> tuple[BannedIP]:
    return await get_object_from_db(BannedIP, filter=filter, limit=limit, session=session)
