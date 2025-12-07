from typing import override

from sqlalchemy.ext.asyncio import AsyncSession

from database.models import App
from .base import Repository


class AppRepo(Repository):
    def __init__(self):
        super().__init__(App)
