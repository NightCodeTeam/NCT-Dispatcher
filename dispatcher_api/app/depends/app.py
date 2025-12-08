from typing import Annotated

from fastapi import Depends, HTTPException, status, Body

from core.debug import logger
from database import DB
from database.models import App
from .session import SessionDep


async def get_app(session: SessionDep, app_name: str = Body(), code: str = Body()) -> App:
    app = await DB.apps.by_name_code(
        name=app_name,
        code=code,
        session=session
    )
    print('>>>>>>>>>>>>>>>>>>>>>>>>>', app)
    print(await DB.apps.all(session=session))
    if app is not None:
        return app
    logger.error(f'Cant find app: {app_name} - {code}')
    raise HTTPException(
        detail='Required app fields are incorrect',
        status_code=status.HTTP_400_BAD_REQUEST
    )


AppDep = Annotated[App, Depends(get_app)]
