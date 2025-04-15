from operator import eq
from re import L
from database.models import Incident, App

from .bot_dataclasses import BotMessage, BotInlineKeyboardLine, BotReplyMarkup
from .reply_markup import incident_markup

from .bot_settings import BotCallbacks
from settings import settings


class BotAdminChat(BotMessage):
    def __init__(
        self,
        text: str,
        message_id: int | None = None,
        reply_to_message_id: int | None = None,
        reply_markup: BotReplyMarkup | None = None,
    ):
        super().__init__(
            chat_id=settings.TELEGRAM_ADMIN_CHAT,
            text=text,
            message_id=message_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup,
            parse_mode="MarkdownV2"
        )


class BotBackButton(BotInlineKeyboardLine):
    def __init__(self):
        super().__init__(
            text='<- назад',
            callback_data=BotCallbacks.BACK
        )


class BotNewIncidentMessage(BotAdminChat):
    def __init__(
        self,
        app_name: str,
        title: str,
        message: str,
        level: str,
        logs: str,
        incident_id: int,
        back: bool = False,
        message_id: int | None = None,
    ):
        lines = [[
            BotInlineKeyboardLine(
                text="Закрыть",
                callback_data=f'{BotCallbacks.CLOSE_INCIDENT}{incident_id}'
            ),
            BotInlineKeyboardLine(
                text="Удалить",
                callback_data=f'{BotCallbacks.DEL_INCIDENT}{incident_id}'
            ),
        ]]
        if back:
            lines.append(
                [BotBackButton()]
            )
        super().__init__(
            text=f'{app_name}\n{title}\n{level}\n\n{message}\n```txt\n{logs}\n```',
            reply_markup=BotReplyMarkup(
                inline_keyboard=lines
            ),
            message_id=message_id
        )


class BotError(BotAdminChat):
    def __init__(self, error_message: str):
        super().__init__(
            text=f"Произошла ошибка:\n```txt\n{error_message}\n```",
        )


class BotIncedentClosed(BotAdminChat):
    def __init__(self, message_id: int, incident_title: str):
        super().__init__(
            text=f"Инцидент {incident_title} закрыт",
            message_id=message_id,
            reply_markup=BotReplyMarkup(
                [[BotBackButton()]]
            )
        )


class BotIncedentDeleted(BotAdminChat):
    def __init__(self, message_id: int, incident_title: str):
        super().__init__(
            text=f"Инцидент {incident_title} удален",
            message_id=message_id,
            reply_markup=BotReplyMarkup(
                [[BotBackButton()]]
            )
        )


class BotAppDeleted(BotAdminChat):
    def __init__(self, message_id: int, app_name: str):
        super().__init__(
            text=f"Приложение {app_name} удалено",
            message_id=message_id,
            reply_markup=BotReplyMarkup(
                [[BotBackButton()]]
            )
        )


class BotStartMessage(BotAdminChat):
    def __init__(self, new_incedents_len: int, message_id: int):
        super().__init__(
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
            ])
        )


class BotBackMessage(BotAdminChat):
    def __init__(self, new_incedents_len: int, message_id: int):
        super().__init__(
            text=f'Новых инцедентов: {new_incedents_len}',
            message_id=message_id,
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
            ])
        )


class BotShowIncidents(BotAdminChat):
    def __init__(self, message_id: int, incidents: list[Incident] | tuple[Incident]):
        lines = [[
            BotInlineKeyboardLine(
                text=incident.title,
                callback_data=f'{BotCallbacks.SELECT_INCIDENT}{incident.id}'
            )
        ] for incident in incidents]
        lines.append([BotBackButton()])
        super().__init__(
            text=f'Список инцидентов:',
            message_id=message_id,
            reply_markup=BotReplyMarkup(lines)
        )


class BotShowApps(BotAdminChat):
    def __init__(self, message_id: int, apps: list[App] | tuple[App]):
        lines = [[
            BotInlineKeyboardLine(
                text=app.name,
                callback_data=f'{BotCallbacks.SELECT_APP}{app.id}'
            )
        ] for app in apps]
        lines.append([BotBackButton()])
        super().__init__(
            text=f'Список приложений:',
            message_id=message_id,
            reply_markup=BotReplyMarkup(lines)
        )


class BotSelectedApp(BotAdminChat):
    def __init__(self, message_id: int, app: App):
        lines = [[
            BotBackButton(),
            BotInlineKeyboardLine(
                text='Удалить',
                callback_data=f'{BotCallbacks.DEL_APP}{app.id}'
            )
        ],
        [
            BotInlineKeyboardLine(
                text='Инциденты',
                callback_data=f'{BotCallbacks.SELECT_APP_INCIDENTS}{app.id}'
            )
        ]]
        super().__init__(
            text=f'Название: {app.name}\nCode: `{app.dispatcher_code}`\nURL: ',
            message_id=message_id,
            reply_markup=BotReplyMarkup(lines)
        )


class BotSelectedIncident(BotNewIncidentMessage):
    def __init__(self, message_id: int, app: App, incident: Incident):
        super().__init__(
            app_name=app.name,
            title=incident.title,
            message=incident.message,
            level=incident.level,
            logs=incident.logs,
            incident_id=incident.id,
            back=True,
            message_id=message_id
        )


class BotNewAppMessageOLD(BotAdminChat):
    def __init__(self, message_id: int):
        super().__init__(
            text=f'Создание нового приложения:',
            message_id=message_id,
            reply_markup=BotReplyMarkup([
                [
                    BotInlineKeyboardLine(
                        text='Название:',
                        switch_inline_query_current_chat=BotCallbacks.NEW_APP_NAME,
                    )
                ],
                [
                    BotInlineKeyboardLine(
                        text='URL:',
                        switch_inline_query_current_chat=BotCallbacks.NEW_APP_URL,
                    )
                ],
                [
                    BotInlineKeyboardLine(
                        text='ПОДТВЕРДИТЬ!:',
                        callback_data=BotCallbacks.BACK,
                    )
                ],
                [BotBackButton()],
            ])
        )


class BotNewAppMessage(BotAdminChat):
    def __init__(self, name, url, code):
        super().__init__(
            text=f'Создано новое приложение\nНазвание: {name}\nURL: не отображается\nКод доступа: `{code}`',
        )