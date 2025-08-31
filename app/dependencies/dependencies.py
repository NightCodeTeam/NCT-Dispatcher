from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import App
from database.repo import DB

from core.debug import create_log
from database.session import get_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def get_app(request: Request, session: SessionDep) -> App | None:
    res_json = await request.json()
    app = await DB.apps.get_app_by_name_code(
        name=res_json.get('app_name'),
        code=res_json.get('dispatcher_code'),
        session=session
    )
    if app:
        return app
    create_log(f'cant find app {res_json.get('app_name')}', 'error')
    return None


AppDep = Annotated[App | None, Depends(get_app)]