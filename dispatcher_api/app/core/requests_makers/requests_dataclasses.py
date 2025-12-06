from dataclasses import dataclass
from datetime import datetime
from typing import Literal


Method = Literal['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'OPTIONS']
AllowedMethods = ('GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'OPTIONS')


@dataclass(frozen=True, slots=True)
class ResponseData:
    url: str
    status: int
    headers: dict
    json: dict
    time: datetime = datetime.now()
