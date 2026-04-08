import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status, Body

from database.models import App
from .db import DBDep


async def get_app(database: DBDep, app_name: str = Body(), code: str = Body()) -> App:
    app = await database.apps.by_name_code(
        name=app_name,
        code=code,
    )
    if app is not None:
        return app
    logging.error(f'Cant find app: {app_name} - {code}')
    raise HTTPException(
        detail='Required app fields are incorrect',
        status_code=status.HTTP_400_BAD_REQUEST
    )


AppDep = Annotated[App, Depends(get_app)]
