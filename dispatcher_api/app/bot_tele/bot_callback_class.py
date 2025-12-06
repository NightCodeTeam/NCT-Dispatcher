from core.debug import create_log
from database.utils import get_incidents_from_db, get_apps_from_db, get_banned_ips_from_db
from database.repo import DB
from database.session import new_session
from .bot_dataclasses import UpdateCallback
from .bot_requests import HttpTeleBot
from .bot_parser import parse_bot_callback_id
from .bot_exceplions import BotMessageNoneException, BotCallbackDataNoneException
from .bot_additional_classes import (
    BotBackMessage,
    BotError,
    BotIncidentClosed,
    BotIncidentDeleted,
    BotAppDeleted,
    BotShowIncidents,
    BotShowApps,
    BotSelectedApp,
    BotSelectedIncident,
    BotBanDeleted,
    BotShowBans,
    BotSelectedBan,
)


class TeleBotCallbacks:
    def __init__(self, client: HttpTeleBot):
        self.client = client

    # ! Проверка на id сообщения
    @staticmethod
    def message_is_none_check(func):
        async def wrapper(*args, **kwargs):
            update: UpdateCallback | None = None
            try:
                if type(args[1]):
                    update = args[1]
            except IndexError:
                update = kwargs.get('update')
            if update is None:
                create_log(f'Update is None in {func.__name__}', 'error')
                return None

            if update.callback_query.message is not None and update.callback_query.message.message_id:
                return await func(*args, **kwargs)
            create_log(f'Message is None: {update.callback_query}', 'info')
            return None
        return wrapper

    async def back(self, update: UpdateCallback):
        create_log(f'command_back > {update}', 'debug')
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        incidents = len(await DB.incidents.only_open())
        await self.client.edit_message_text(
            BotBackMessage(incidents, message_id=update.callback_query.message.message_id)
        )

    # ! Инциденты
    async def all_incidents(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        incidents = await DB.incidents.all(limit=95)
        await self.client.edit_message_text(BotShowIncidents(
            message_id=update.callback_query.message.message_id,
            incidents=incidents
        ))

    async def open_incidents(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        incidents = await DB.incidents.only_open(limit=80)
        await self.client.edit_message_text(BotShowIncidents(
            message_id=update.callback_query.message.message_id,
            incidents=incidents
        ))

    async def select_incident(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)
        incident = await DB.incidents.get_incident_by_id(parse_bot_callback_id(update.callback_query.data))
        if incident:
            app = await DB.apps.get_app_by_id(incident.app_id)
            if app:
                return await self.client.edit_message_text(BotSelectedIncident(
                    message_id=update.callback_query.message.message_id,
                    app=app,
                    incident=incident
                ))
            return await self.client.sent_msg(BotError(f'Приложение не найдено {incident.app_id}'))
        return await self.client.sent_msg(BotError(f'Инцидент не найден {parse_bot_callback_id(update.callback_query.data)}'))

    async def close_incident(self, update: UpdateCallback):
        create_log('close_incident >', 'debug')
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)
        async with new_session() as session:
            incident_id = parse_bot_callback_id(update.callback_query.data)
            if incident_id is not None:
                incident = await DB.incidents.get_incident_by_id(incident_id, session)
                incident.status = 'closed'
                await session.commit()

                await self.client.edit_message_text(
                    BotIncidentClosed(update.callback_query.message.message_id, incident.title)
                )
            else:
                create_log(f'Invalid incident ID: {incident_id} : {update}', 'error')
                await self.client.sent_msg(BotError(f'Невозможно закрыть инцедент: не найден {incident_id}'))

    async def del_incident(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)
        async with new_session() as session:
            incident_id = parse_bot_callback_id(update.callback_query.data)
            if incident_id is not None:
                incident = await DB.incidents.delete_by_id(incident_id, session, True)
                await self.client.edit_message_text(
                    BotIncidentDeleted(update.callback_query.message.message_id, incident.title)
                )
            else:
                create_log(f'Invalid incident ID: {incident_id} : {update}', 'error')
                await self.client.sent_msg(BotError(f'Невозможно удалить инцидент: не найден {incident_id}'))

    # ! Приложения
    async def all_apps(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        apps = await DB.apps.all()
        await self.client.edit_message_text(
            BotShowApps(
                message_id=update.callback_query.message.message_id,
                apps=apps
            )
        )

    async def select_app(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)
        app = await DB.apps.get_app_by_id(parse_bot_callback_id(update.callback_query.data))
        await self.client.edit_message_text(BotSelectedApp(
            message_id=update.callback_query.message.message_id,
            app=app
        ))

    async def app_selected_incidents(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)
        incidents = await DB.incidents.get_by_app_id(parse_bot_callback_id(update.callback_query.data))
        await self.client.edit_message_text(BotShowIncidents(
            message_id=update.callback_query.message.message_id,
            incidents=incidents
        ))

    async def new_app_confirm(self, update: UpdateCallback):
        pass

    async def new_app_cancel(self, update: UpdateCallback):
        pass

    async def del_app(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)

        async with new_session() as session:
            app_id = parse_bot_callback_id(update.callback_query.data)
            if app_id is not None:
                await DB.apps.delete_by_id(app_id, session, True)
                await self.client.edit_message_text(
                    BotAppDeleted(update.callback_query.message.message_id, str(app_id))
                )
            else:
                create_log(f'Invalid incident ID: {app_id} : {update}', 'error')
                await self.client.sent_msg(BotError(f'Невозможно удалить инцедент: не найден {app_id}'))

    async def bans(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        await self.client.edit_message_text(BotShowBans(
            message_id=update.callback_query.message.message_id,
            bans = await DB.banned_ips.all(limit=90)
        ))

    async def select_ban(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)
        await self.client.edit_message_text(BotSelectedBan(
            message_id=update.callback_query.message.message_id,
            ban=await DB.banned_ips.get_ip_by_ip(parse_bot_callback_id(update.callback_query.data))
        ))

    async def del_ban(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)

        async with new_session() as session:
            ban_id = parse_bot_callback_id(update.callback_query.data)
            if ban_id is not None:
                ban = await get_apps_from_db(f'bannedips.id = {ban_id}', session=session)
                ban = ban[0]
                await session.delete(ban)
                await session.commit()

                await self.client.edit_message_text(
                    BotBanDeleted(update.callback_query.message.message_id, ban.name)
                )
            else:
                create_log(f'Invalid ban ID: {ban_id} : {update}', 'error')
                await self.client.sent_msg(BotError(f'Невозможно удалить бан: не найден {ban_id}'))