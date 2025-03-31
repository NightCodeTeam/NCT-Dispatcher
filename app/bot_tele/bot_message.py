from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BotInlineKeyboardLine:
    text: str
    callback_data: str | None = None
    switch_inline_query_current_chat: str | None = None


@dataclass(frozen=True, slots=True)
class BotReplyMarkup:
    inline_keyboard: list[BotInlineKeyboardLine|list[BotInlineKeyboardLine]]


@dataclass(frozen=True, slots=True)
class BotMessage:
    chat_id: int
    text: str
    reply_to_message_id: int | None = None
    reply_markup: dict | None = None
