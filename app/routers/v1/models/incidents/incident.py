from pydantic import BaseModel

from core.debug.debug_dataclass import Level


class IncidentRequest(BaseModel):
    name: str
    log: str

    app_name: str
    level: Level
