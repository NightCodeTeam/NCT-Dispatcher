from typing import List, Literal
from pydantic import BaseModel

from core.debug.debug_dataclass import Level


class IncidentRequest(BaseModel):
    title: str
    message: str
    logs: str
    level: Level


class NewStatusRequest(BaseModel):
    new_status: Literal['open', 'closed']


class MultipleIncidentResponse(BaseModel):
    incidents: List[IncidentResponse]


class IncidentResponse(BaseModel):
    title: str
    message: str
    logs: str
    level: Level
    status: str
    app_name: str
