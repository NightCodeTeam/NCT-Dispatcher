from dataclasses import dataclass
from typing import Literal


Method = Literal['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'PATCH', 'OPTIONS']


@dataclass(frozen=True, slots=True)
class ResponseData:
    json: dict
