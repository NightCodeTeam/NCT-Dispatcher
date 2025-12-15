from dataclasses import dataclass
from .user_dataclasses import User
from .message_dataclasses import Message


@dataclass(frozen=True, slots=True)
class CallbackQuery:
    id: int
    from_user: User
    chat_instance: int
    message: Message | None = None
    data: str | None = None
