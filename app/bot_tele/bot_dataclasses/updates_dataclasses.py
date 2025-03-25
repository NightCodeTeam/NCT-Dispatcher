from dataclasses import dataclass
from .callbacks_dataclasses import CallbackQuery
from .message_dataclasses import Message


@dataclass(frozen=True, slots=True)
class Update:
    update_id: int


@dataclass(frozen=True, slots=True)
class UpdateMessage(Update):
    message: Message


@dataclass(frozen=True, slots=True)
class UpdateCallback(Update):
    callback_query: CallbackQuery
