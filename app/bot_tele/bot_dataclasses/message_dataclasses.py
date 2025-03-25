from __future__ import annotations
from dataclasses import dataclass

from .entity_dataclasses import Entity
from .chat_dataclasses import Chat
from .user_dataclasses import User


@dataclass(frozen=True, slots=True)
class Message:
    message_id: int
    message_thread_id: int | None # Если это суппергруппа
    date: int
    chat: Chat
    from_user: User | None = None
    reply_to_message: Message | None = None # Является ответом на сообщение
    text: str | None = None
    entities: tuple[Entity, ...] | None = None
    new_chat_members: tuple[User, ...] | None = None
    left_chat_member: tuple[User, ...] | None = None
