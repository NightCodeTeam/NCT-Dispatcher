from os import stat
from fastapi import APIRouter, Request, Response, status
from sqlalchemy import select
from pydantic import BaseModel

from core.debug import create_log
from dependencies.dependencies import SessionDep, AppDep
from database.models import App, Incident
from bot_tele.bot_requests import HttpTeleBot
from bot_tele.bot_additional_classes import BotNewIncidentMessage, BotError
from .models import IncidentRequest

from settings import settings


router = APIRouter(prefix=settings.INCIDENTS_API_PATH)
bot = HttpTeleBot()


@router.post('/post_incident')
async def post_incident(incident: IncidentRequest, app: AppDep, session: SessionDep):
    try:
        create_log(f'> post incident: {incident}, {app}, {session}', 'debug')
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
        create_log(f'App error: {app} req app: {incident}', 'error')
        await bot.sent_msg(
            BotError(
                error_message=f'Приложение не найдено:\n{incident}'
            )
        )
        return Response(status_code=400)
    except Exception as e:
        BotError(
            error_message=str(e)
        )
        await session.rollback()
        create_log(f'Error in post_incident, {e}', 'error')

