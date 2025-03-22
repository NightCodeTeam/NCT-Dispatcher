from typing import Annotated
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.models.app import App

from database.session import get_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def get_app(request: Request, session: SessionDep) -> App | None:
    res = await session.execute(select(App).where(
        App.name == request.headers.get('app'),
        App.dispatcher_code == request.headers.get('dispatch')
    ))
    if res.first() is not None:
        return res.first()[0]


AppDep = Annotated[App | None, Depends(get_app)]