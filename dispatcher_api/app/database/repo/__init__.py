from .incident import IncidentRepo
from .app import AppRepo


class DB:
    apps = AppRepo()
    incidents = IncidentRepo()


__all__ = (
    'DB',
)
