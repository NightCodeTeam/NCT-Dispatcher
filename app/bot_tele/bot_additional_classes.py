from re import L
from database.models import Incident, App

from .bot_dataclasses import BotMessage, BotInlineKeyboardLine, BotReplyMarkup
from .reply_markup import incident_markup

from .bot_settings import BotCallbacks
from settings import settings


class BotNewIncidentMessage(BotMessage):
    def __init__(self, app_name: str, title: str, message: str, level: str, logs: str, incident_id: int):
        super().__init__(
            chat_id=settings.TELEGRAM_ADMIN_CHAT,
            text=f'{app_name}\n{title}\n{level}\n\n{message}\n```txt\n{logs}\n```',
            reply_markup=BotReplyMarkup(
                inline_keyboard=[[
                    BotInlineKeyboardLine(
                        text="Закрыть",
                        callback_data=f'{BotCallbacks.CLOSE_INCIDENT}{incident_id}'
                    ),
                    BotInlineKeyboardLine(
                        text="Удалить",
                        callback_data=f'{BotCallbacks.DEL_INCIDENT}{incident_id}'
                    ),
                ]]
            ),
            parse_mode="MarkdownV2",
        )

class BotError(BotMessage):
    def __init__(self, error_message: str):
        super().__init__(
            chat_id=settings.TELEGRAM_ADMIN_CHAT,
            text=f"Произошла ошибка:\n```txt\n{error_message}\n```",
            parse_mode="MarkdownV2",
        )


class BotIncedentClosed(BotMessage):
    def __init__(self, message_id: int, incident_title: str):
        super().__init__(
            chat_id=settings.TELEGRAM_ADMIN_CHAT,
            text=f"Инцидент {incident_title} закрыт",
            message_id=message_id,
            parse_mode="MarkdownV2",
        )


class BotIncedentDeleted(BotMessage):
    def __init__(self, message_id: int, incident_title: str):
        super().__init__(
            chat_id=settings.TELEGRAM_ADMIN_CHAT,
            text=f"Инцидент {incident_title} удален",
            message_id=message_id,
            parse_mode="MarkdownV2",
        )


class BotStartMessage(BotMessage):
    def __init__(self, new_incedents_len: int, message_id: int):
        super().__init__(
            chat_id=settings.TELEGRAM_ADMIN_CHAT,
            text=f'Новых инцедентов: {new_incedents_len}',
            reply_to_message_id=message_id,
            reply_markup=BotReplyMarkup([
                [
                    BotInlineKeyboardLine(
                        text='Новые инциденты',
                        callback_data=BotCallbacks.OPEN_INCIDENTS
                    )
                ],
                [
                    BotInlineKeyboardLine(
                        text='Список всех инцидентов',
                        callback_data=BotCallbacks.ALL_INCIDENTS
                    )
                ],
                [
                    BotInlineKeyboardLine(
                        text='Все приложения',
                        callback_data=BotCallbacks.ALL_APPS
                    )
                ],
                [
                    BotInlineKeyboardLine(
                        text='Новое приложение',
                        callback_data=BotCallbacks.NEW_APP
                    )
                ]
            ])
        )

class BotShowIncidents(BotMessage):
    def __init__(self, message_id: int, incidents: list[Incident] | tuple[Incident]):
        lines = [[
            BotInlineKeyboardLine(
                text=incident.title,
                callback_data=f'{BotCallbacks.SELECT_INCIDENT}{incident.id}'
            )
        ] for incident in incidents]
        lines.append([
            BotInlineKeyboardLine(
                text='<- ВЕРНУТЬСЯ',
                callback_data=BotCallbacks.BACK
            )
        ])
        super().__init__(
            chat_id=settings.TELEGRAM_ADMIN_CHAT,
            text=f'Список инцидентов:',
            message_id=message_id,
            parse_mode="MarkdownV2",
            reply_markup=BotReplyMarkup(lines)
        )


class BotShowApps(BotMessage):
    def __init__(self, message_id: int, apps: list[App] | tuple[App]):
        lines = [[
            BotInlineKeyboardLine(
                text=app.name,
                callback_data=f'{BotCallbacks.SELECT_APP}{app.id}'
            )
        ] for app in apps]
        lines.append([
            BotInlineKeyboardLine(
                text='<- ВЕРНУТЬСЯ',
                callback_data=BotCallbacks.BACK
            )
        ])
        super().__init__(
            chat_id=settings.TELEGRAM_ADMIN_CHAT,
            text=f'Список приложений:',
            message_id=message_id,
            parse_mode="MarkdownV2",
            reply_markup=BotReplyMarkup(lines)
        )


