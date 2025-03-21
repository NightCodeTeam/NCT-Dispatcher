from pydantic import BaseModel
from typing import Literal
from enum import Enum
from app.core.debug.debug_dataclass import Level


class IncidentRequest(BaseModel):
    name: str
    log: str

    app_name: str
    level: Level
