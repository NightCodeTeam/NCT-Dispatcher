from pydantic import BaseModel
from core.debug.debug_dataclass import Level


class Incident(BaseModel):
    title: str
    message: str
    logs: list[str]
    level: Level
    status: str = "open"
