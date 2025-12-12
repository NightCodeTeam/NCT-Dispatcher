from typing import TypeVar
from database.database import Base
from database.session import new_session


T = TypeVar('T', bound=Base)
