from core.debug import create_log
from database.utils import get_incidents_from_db, get_apps_from_db, get_banned_ips_from_db
from database.session import connect_session, get_session, new_session
from .bot_dataclasses import UpdateCallback
from .bot_requests import HttpTeleBot
from .bot_parser import parse_bot_callback_id
from .bot_exceplions import BotMessageNoneException, BotCallbackDataNoneException
from .bot_additional_classes import (
    BotStartMessage,
    BotBackMessage,
    BotError,
    BotIncedentClosed,
    BotIncedentDeleted,
    BotAppDeleted,
    BotShowIncidents,
    BotShowApps,
    BotSelectedApp,
    BotSelectedIncident,
    BotNewAppMessage,
    BotBanDeleted,
    BotShowBans,
    BotSelectedBan,
)

#from text_messages import


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
        create_log(f'command_start > {update}', 'debug')
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        #create_log(f'>>> {update.callback_query.message.message_id}', 'info')
        incedents = len(await get_incidents_from_db('incidents.status = "open"'))
        await self.client.edit_message_text(
            BotBackMessage(incedents, message_id=update.callback_query.message.message_id)
        )

    # ! Инцеденты
    async def all_incidents(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        #create_log(f'>>> {update.callback_query.message.message_id}', 'info')
        incidents = await get_incidents_from_db(limit=90)
        await self.client.edit_message_text(BotShowIncidents(
            message_id=update.callback_query.message.message_id,
            incidents=incidents
        ))

    async def open_incidents(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        incidents = await get_incidents_from_db('incidents.status = "open"', limit=90)
        await self.client.edit_message_text(BotShowIncidents(
            message_id=update.callback_query.message.message_id,
            incidents=incidents
        ))

    async def select_incident(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)
        incident = await get_incidents_from_db(f'incidents.id={parse_bot_callback_id(update.callback_query.data)}')
        app = await get_apps_from_db(f'apps.id={incident[0].app_id}')
        await self.client.edit_message_text(BotSelectedIncident(
            message_id=update.callback_query.message.message_id,
            app=app[0],
            incident=incident[0]
        ))

    async def close_incident(self, update: UpdateCallback):
        create_log('close_incident >', 'debug')
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)
        async with new_session() as session:
            incident_id = parse_bot_callback_id(update.callback_query.data)
            if incident_id is not None:
                incident = (await get_incidents_from_db(f'incidents.id = {incident_id}', session=session))[0]
                incident.status = 'closed'
                await session.commit()

                await self.client.edit_message_text(
                    BotIncedentClosed(update.callback_query.message.message_id, incident.title)
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
                incident = (await get_incidents_from_db(f'incidents.id = {incident_id}', session=session))[0]
                await session.delete(incident)
                await session.commit()

                await self.client.edit_message_text(
                    BotIncedentDeleted(update.callback_query.message.message_id, incident.title)
                )
            else:
                create_log(f'Invalid incident ID: {incident_id} : {update}', 'error')
                await self.client.sent_msg(BotError(f'Невозможно удалить инцедент: не найден {incident_id}'))

    # ! Приложения
    async def all_apps(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        apps = await get_apps_from_db()
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
        app = await get_apps_from_db(f'apps.id={parse_bot_callback_id(update.callback_query.data)}')
        await self.client.edit_message_text(BotSelectedApp(
            message_id=update.callback_query.message.message_id,
            app=app[0]
        ))

    async def app_selected_incidents(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)
        incidents = await get_incidents_from_db(
            f'incidents.app_id={parse_bot_callback_id(update.callback_query.data)}'
        )
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
                app = await get_apps_from_db(f'apps.id = {app_id}', session=session)
                app = app[0]
                await session.delete(app)
                await session.commit()

                await self.client.edit_message_text(
                    BotAppDeleted(update.callback_query.message.message_id, app.name)
                )
            else:
                create_log(f'Invalid incident ID: {app_id} : {update}', 'error')
                await self.client.sent_msg(BotError(f'Невозможно удалить инцедент: не найден {app_id}'))

    async def bans(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        bans = await get_banned_ips_from_db(limit=90)
        await self.client.edit_message_text(BotShowBans(
            message_id=update.callback_query.message.message_id,
            bans=bans
        ))

    async def select_ban(self, update: UpdateCallback):
        if update.callback_query.message is None:
            raise BotMessageNoneException(update)
        if update.callback_query.data is None:
            raise BotCallbackDataNoneException(update)
        ban = await get_banned_ips_from_db(f'bannedips.id={parse_bot_callback_id(update.callback_query.data)}')
        await self.client.edit_message_text(BotSelectedBan(
            message_id=update.callback_query.message.message_id,
            ban=ban[0]
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