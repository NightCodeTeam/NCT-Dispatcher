from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class Chat:
    id: int
    type: Literal['private', 'group', 'supergroup', 'channel']
    title: str = ''
    username: str = ''
    first_name: str = ''
    last_name: str = ''
    is_forum: bool = False
