from fastapi import APIRouter, HTTPException

from src.core.pydantic_misc_models import Ok
from src.core.fast_decorators import cache, rate_limiter
from src.core.redis_client import RedisDep
from src.depends import UserDep, DBDep, AppDep
from src.core.fast_depends import PaginationParams
from src.core.debug import logger
from src.core.telegrambot import TeleBot, BotMessage
from src.core.sql_repository import ItemNotFound
from src.services.authservice import AuthService
from .models import IncidentRequest, MultipleIncidentResponse, IncidentResponse
from .models import NewStatusRequest

from settings import settings


incidents_router_v1 = APIRouter(prefix='/v1/incidents', tags=['incidents'])
bot = TeleBot(
    token=settings.TELEGRAM_BOT_TOKEN,
    commands={},
    callbacks={},
)


@incidents_router_v1.get('/', response_model=MultipleIncidentResponse)
@cache(key='incidents:all_incident')
@rate_limiter(max_requests=10, time_delta=30)
async def all_incidents(db: DBDep, pagination: PaginationParams, user: UserDep, redis: RedisDep):
    if pagination.limit is not None and pagination.skip is not None:
        incidents = await db.incidents.pagination(
            skip=pagination.skip,
            limit=pagination.limit,
            load_relations=True,
        )
    else:
        incidents = await db.incidents.all(load_relations=True)
    return {'incidents': [{
        'id': i.id,
        'title': i.title,
        'message': i.message,
        'logs': i.logs,
        'level': i.level,
        'status': i.status,
        'app_name': i.src.name,
        'created_at': i.created_at,
        'updated_at': i.updated_at,
        'edit_by_user': await AuthService().user_by_id(
            i.edit_by_id, redis
        ) if i.edit_by_id else None
    } for i in incidents]}


@incidents_router_v1.post('/new', response_model=Ok)
async def post_incident(incident: IncidentRequest, app: AppDep, db: DBDep):
    if not settings.DEBUG:
        await bot.client.sent_msg(BotMessage(
            chat_id=settings.TELEGRAM_CHAT_ID,
            text=f'Новый инцидент: {incident.title} ({src.name})\n{incident.message}'
        ))
    return {'ok': await db.incidents.new(
        title=incident.title,
        message=incident.message,
        logs=incident.logs,
        level=incident.level,
        app_id=src.id,
        commit=True
    )}


@incidents_router_v1.get('/{incident_id}', response_model=IncidentResponse)
@cache(key='incidents:by_id')
@rate_limiter(max_requests=10, time_delta=30)
async def incident_by_id(db: DBDep, user: UserDep, incident_id: int, redis: RedisDep):
    inc = await db.incidents.by_id(incident_id=incident_id, load_relations=True)
    if inc is None:
        raise HTTPException(status_code=404, detail=f'Incident {incident_id} not found')
    return {
        'id': inc.id,
        'title': inc.title,
        'message': inc.message,
        'logs': inc.logs,
        'level': inc.level,
        'status': inc.status,
        'app_name': inc.src.name,
        'created_at': inc.created_at,
        'updated_at': inc.updated_at,
        'edit_by_user': await AuthService().user_by_id(inc.edit_by_id, redis) if inc.edit_by_id else None
    }


@incidents_router_v1.delete('/{incident_id}', response_model=Ok)
async def del_incident_by_id(db: DBDep, user: UserDep, incident_id: int):
    try:
        return {'ok': await db.incidents.del_by_id(
            incident_id=incident_id,
            commit=True,
        )}
    except ItemNotFound:
        raise HTTPException(status_code=404, detail='Incident not found')


@incidents_router_v1.put('/{incident_id}/status', response_model=Ok)
async def update_status(
    db: DBDep,
    user: UserDep,
    incident_id: int,
    status_req: NewStatusRequest
):
    try:
        return {'ok': await db.incidents.update_status(
            incident_id=incident_id,
            new_status=status_req.new_status,
            updated_by_id=user.id,
        )}
    except ItemNotFound:
        raise HTTPException(status_code=404, detail='Incident not found')
