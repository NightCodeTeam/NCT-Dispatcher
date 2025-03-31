from core.debug import create_log
from database.utils import get_incidents_from_db, get_apps_from_db
from database.session import connect_session, get_session, new_session
from .bot_dataclasses import UpdateCallback
from .bot_requests import HttpTeleBot
from .bot_parser import parse_bot_callback_id

#from text_messages import


class TeleBotCallbacks:
    def __init__(self, client: HttpTeleBot):
        self.client = client

    # ! Инцеденты
    async def select_incident(self, update: UpdateCallback):
        pass

    async def close_incident(self, update: UpdateCallback):
        async with new_session() as session:
            incident_id = parse_bot_callback_id(update.callback_query.data)
            if incident_id is not None:
                incident = (await get_incidents_from_db(f'incidents.id = {incident_id}', session=session))[0]
                incident.status = 'closed'
                await session.commit()
            else:
                create_log(f'Invalid incident ID: {incident_id} : {update}', 'error')


    async def del_incident(self, update: UpdateCallback):
        async with new_session() as session:
            incident_id = parse_bot_callback_id(update.callback_query.data)
            if incident_id is not None:
                incident = (await get_incidents_from_db(f'incidents.id = {incident_id}', session=session))[0]
                await session.delete(incident)
                await session.commit()
            else:
                create_log(f'Invalid incident ID: {incident_id} : {update}', 'error')

    # ! Приложения
    async def all_apps(self, update: UpdateCallback):
        pass

    async def new_app(self, update: UpdateCallback):
        pass

    async def new_app_confirm(self, update: UpdateCallback):
        pass

    async def new_app_cancel(self, update: UpdateCallback):
        pass

    async def select_app(self, update: UpdateCallback):
        pass
