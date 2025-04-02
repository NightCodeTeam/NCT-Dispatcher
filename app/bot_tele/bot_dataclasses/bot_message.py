import json
from typing import Literal
from dataclasses import dataclass, asdict

@dataclass(frozen=True, slots=True)
class BotInlineKeyboardLine:
    text: str
    callback_data: str | None = None
    switch_inline_query_current_chat: str | None = None


@dataclass(frozen=True, slots=True)
class BotReplyMarkup:
    inline_keyboard: list[list[BotInlineKeyboardLine]]


@dataclass(frozen=True, slots=True)
class BotMessage:
    chat_id: int
    message_id: int | None = None
    text: str = ''
    reply_to_message_id: int | None = None
    reply_markup: BotReplyMarkup | None = None

    parse_mode: Literal["HTML", "Markdown", "MarkdownV2"] | None = None

    @property
    def to_dict(self) -> dict:
        params = {
            "chat_id": self.chat_id,
            "text": self.text,
        }
        if self.message_id is not None:
            params["message_id"] = self.message_id
        if self.reply_to_message_id is not None:
            params["reply_to_message_id"] = self.reply_to_message_id
        if self.reply_markup is not None:
            params["reply_markup"] = json.dumps(asdict(self.reply_markup))
        if self.parse_mode is not None:
            params["parse_mode"] = self.parse_mode
        return params