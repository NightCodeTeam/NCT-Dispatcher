from .incident import IncidentRepo
from .app import AppRepo
from .user import UserRepo


class DB:
    apps = AppRepo()
    incidents = IncidentRepo()
    users = UserRepo()


__all__ = (
    'DB',
)
