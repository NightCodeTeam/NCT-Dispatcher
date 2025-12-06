import logging
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import App
from database.repo import DB

from database.session import get_session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
