from fastapi import APIRouter, Response

from core.debug import create_log
from dependencies.dependencies import SessionDep, AppDep
from database.models import Incident
from database.repo import DB
from bot_tele.bot_requests import HttpTeleBot
from bot_tele.bot_additional_classes import BotNewIncidentMessage, BotError
from .models import IncidentRequest


router = APIRouter(prefix='/incidents')
bot = HttpTeleBot()


@router.post('/incident')
async def post_incident(incident: IncidentRequest, app: AppDep, session: SessionDep):
    try:
        if app:
            create_log(f'>new incident: {incident.title} - {app.name}', 'debug')
            new_incident = Incident(
                title=incident.title,
                message=incident.message,
                logs=incident.logs,
                level=incident.level,
                app_id=app.id,
            )
            await DB.incidents.add(new_incident, session, True)
            return {'ok': await bot.sent_msg(
                BotNewIncidentMessage(
                    app_name=app.name,
                    title=incident.title,
                    message=incident.message,
                    logs=incident.logs,
                    level=incident.level,
                    incident_id=new_incident.id
                )
            )}
        create_log(f'App not found: {incident.app_name}', 'error')
        await bot.sent_msg(
            BotError(
                error_message=f'Новый инцидент, но приложение не найдено:\n{incident.title}\n{incident.message}'
            )
        )
        return Response(status_code=400)
    except Exception as e:
        BotError(
            error_message=f'Ошибка в диспатчере: {str(e)}'
        )
        await session.rollback()
        create_log(f'Error in post_incident, {e}', 'error')
