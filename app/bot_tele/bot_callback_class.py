from core.debug import create_log
from database.utils import get_incidents_from_db, get_apps_from_db
from database.session import connect_session, get_session, new_session
from .bot_dataclasses import UpdateCallback
from .bot_requests import HttpTeleBot
from .bot_parser import parse_bot_callback_id
from .bot_additional_classes import (
    BotStartMessage,
    BotError,
    BotIncedentClosed,
    BotIncedentDeleted,
    BotShowIncidents,
    BotShowApps
)

#from text_messages import


class TeleBotCallbacks:
    def __init__(self, client: HttpTeleBot):
        self.client = client

    async def back(self, update: UpdateCallback):
        create_log(f'command_start > {update}', 'debug')
        incedents = len(await get_incidents_from_db('incidents.status = "open"'))
        await self.client.edit_message_text(
            BotStartMessage(incedents, message_id=update.callback_query.message.message_id)
        )

    # ! Инцеденты
    async def all_incidents(self, update: UpdateCallback):
        incidents = await get_incidents_from_db(limit=90)
        await self.client.sent_msg(BotShowIncidents(
            message_id=update.callback_query.message.message_id,
            incidents=incidents
        ))

    async def open_incidents(self, update: UpdateCallback):
        incidents = await get_incidents_from_db('incidents.status = "open"', limit=90)
        await self.client.sent_msg(BotShowIncidents(
            message_id=update.callback_query.message.message_id,
            incidents=incidents
        ))

    async def select_incident(self, update: UpdateCallback):
        pass

    async def close_incident(self, update: UpdateCallback):
        create_log('close_incident >', 'debug')
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
        pass

    async def select_app(self, update: UpdateCallback):
            pass

    async def new_app(self, update: UpdateCallback):
        pass

    async def new_app_confirm(self, update: UpdateCallback):
        pass

    async def new_app_cancel(self, update: UpdateCallback):
        pass
