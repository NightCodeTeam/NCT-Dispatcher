import json
from typing import Literal
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BotInlineKeyboardLine:
    text: str
    callback_data: str | None = None
    switch_inline_query_current_chat: str | None = None

    def to_dict(self) -> dict:
        params = {
            'text': self.text,
        }
        if self.callback_data is not None:
            params['callback_data'] = self.callback_data
        if self.switch_inline_query_current_chat is not None:
            params['switch_inline_query_current_chat'] = self.switch_inline_query_current_chat
        return params


@dataclass(frozen=True, slots=True)
class BotReplyMarkup:
    inline_keyboard: list[list[BotInlineKeyboardLine]]

    def to_dict(self) -> dict:
        lines = []
        for line in self.inline_keyboard:
            sub_line = [sub_line.to_dict() for sub_line in line]
            lines.append(sub_line)
        return {
            'inline_keyboard': lines
        }


@dataclass(frozen=True, slots=True)
class BotMessage:
    chat_id: int
    message_id: int | None = None
    text: str = ''
    reply_to_message_id: int | None = None
    message_thread_id: int | None = None
    reply_markup: BotReplyMarkup | None = None

    parse_mode: Literal["HTML", "Markdown", "MarkdownV2"] = 'MarkdownV2'
    disable_web_page_preview: bool = True

    @property
    def to_dict(self) -> dict:
        params = {
            "chat_id": str(self.chat_id),
            "text": self.text,
        }
        if self.message_id is not None:
            params["message_id"] = self.message_id
        if self.reply_to_message_id is not None:
            params["reply_to_message_id"] = self.reply_to_message_id
        if self.reply_markup is not None:
            params["reply_markup"] = json.dumps(self.reply_markup.to_dict()) # asdict(self.reply_markup)
        if self.parse_mode is not None:
            params["parse_mode"] = self.parse_mode
        params['disable_web_page_preview'] = self.disable_web_page_preview
        return params
