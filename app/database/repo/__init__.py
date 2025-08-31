from .banned_ip import BannedIPRepo
from .incident import IncidentRepo
from .app import AppRepo


class DB:
    apps = AppRepo()
    banned_ips = BannedIPRepo()
    incidents = IncidentRepo()


__all__ = (
    'DB',
)
