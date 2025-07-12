from pydantic import BaseModel

from core.debug.debug_dataclass import Level


class IncidentRequest(BaseModel):
    title: str
    message: str
    logs: str
    level: Level

    app_name: str
    dispatcher_code: str
