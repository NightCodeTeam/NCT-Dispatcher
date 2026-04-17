from typing import List, Literal
from datetime import datetime

from pydantic import BaseModel


class IncidentRequest(BaseModel):
    title: str
    message: str
    logs: str
    level: Literal['debug', 'warning', 'info', 'error', 'crit']


class NewStatusRequest(BaseModel):
    new_status: Literal['open', 'closed']


class IncidentResponse(BaseModel):
    id: int
    title: str
    message: str
    logs: str
    level: Literal['debug', 'warning', 'info', 'error', 'crit']
    status: str
    app_name: str
    created_at: datetime
    updated_at: datetime | None = None
    edit_by_user: str | None = None


class MultipleIncidentResponse(BaseModel):
    incidents: List[IncidentResponse]
