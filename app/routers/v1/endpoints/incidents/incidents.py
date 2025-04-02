from os import stat
from fastapi import APIRouter, Request, Response, status
from sqlalchemy import select
from pydantic import BaseModel

from core.debug import create_log
from routers.v1.models.incidents import IncidentRequest
from dependencies.dependencies import SessionDep, AppDep
from database.models import App, Incident
from bot_tele.bot_requests import HttpTeleBot
from bot_tele.bot_additional_classes import BotNewIncidentMessage, BotError

from settings import settings


router = APIRouter(prefix=settings.INCIDENTS_API_PATH)
bot = HttpTeleBot()


@router.post('/post_incident')
async def post_incident(incident: IncidentRequest, app: AppDep, session: SessionDep):
    try:
        if app is not None:
            new_incident = Incident(
                title=incident.title,
                message=incident.message,
                logs=incident.logs,
                level=incident.level,
                app_id=app.id,
            )
            session.add(new_incident)
            await session.commit()
            await bot.sent_msg(
                BotNewIncidentMessage(
                    app_name=app.name,
                    title=incident.title,
                    message=incident.message,
                    logs=incident.logs,
                    level=incident.level,
                    incident_id=new_incident.id
                )
            )
            return {'ok': True}
        create_log(f'App error: {app} req app: {incident.app_name}', 'error')
        await bot.sent_msg(
            BotError(
                error_message=f'Приложение не найдено\n{incident.title}'
            )
        )
        return Response(status_code=400)
    except Exception as e:
        BotError(
                error_message=str(e)
            )
        await session.rollback()
        create_log(f'Error in post_incident, {e}', 'error')

