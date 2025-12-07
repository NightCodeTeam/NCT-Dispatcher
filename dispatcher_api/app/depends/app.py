import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status

from database import DB
from database.models import App
from .session import SessionDep


async def get_app(app_name: str, code: str, session: SessionDep) -> App:
    app = await DB.apps.by_name_code(
        name=app_name,
        code=code,
        session=session
    )
    if app:
        return app
    logging.error(f'cant find app: {app_name} - {code}')
    raise HTTPException(
            detail='Required app fields are incorrect',
            status_code=status.HTTP_400_BAD_REQUEST
        )


AppDep = Annotated[App, Depends(get_app)]
