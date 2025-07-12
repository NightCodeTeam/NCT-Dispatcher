from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from database.models.app import App

from core.debug import create_log
from database.session import get_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def get_app(request: Request, session: SessionDep) -> App | None:
    data = await request.json()
    res = (await session.execute(
        select(App).where(and_(
            App.dispatcher_code == data.get('dispatcher_code'),
            App.name == data.get('app_name')
        ))
    )).scalars().all()
    if len(res) == 1:
        create_log(f'New request received: app is {res[0].name}', 'info')
        return res[0]
    create_log(f'New request received: app not found', 'error')


AppDep = Annotated[App | None, Depends(get_app)]