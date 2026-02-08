from sqlalchemy.ext.asyncio import AsyncSession

from .incident import IncidentRepo
from .app import AppRepo
from app.core.sql_repository import DataBaseRepo


class DataBase(DataBaseRepo):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.apps = AppRepo(session=session)
        self.incidents = IncidentRepo(session=session)


__all__ = (
    'DataBase',
)
