from typing import List, Literal
from datetime import datetime

from pydantic import BaseModel

from core.debug.debug_dataclass import Level


class IncidentRequest(BaseModel):
    title: str
    message: str
    logs: str
    level: Level


class NewStatusRequest(BaseModel):
    new_status: Literal['open', 'closed']


class IncidentResponse(BaseModel):
    id: int
    title: str
    message: str
    logs: str
    level: Level
    status: str
    app_name: str
    created_at: datetime
    updated_at: datetime | None = None
    edit_by_user: str | None = None


class MultipleIncidentResponse(BaseModel):
    incidents: List[IncidentResponse]
