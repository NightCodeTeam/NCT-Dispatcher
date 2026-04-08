from dataclasses import dataclass
from typing import Literal


EntityTypes = Literal['bot_command', 'mention']


@dataclass(frozen=True, slots=True)
class Entity:
    offset: int
    length: int
    type: EntityTypes
