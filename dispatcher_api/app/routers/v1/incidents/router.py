from fastapi import APIRouter, HTTPException

from core.debug import logger
from database.repo.base import ItemNotFound
from depends import SessionDep, AppDep, TokenDep, PaginationParams
from database import DB
from routers.misc_models import Ok
from bot_tele.bot_requests import HttpTeleBot
from .models import IncidentRequest, MultipleIncidentResponse, IncidentResponse
from .models import NewStatusRequest


incidents_router_v1 = APIRouter(prefix='/v1/incidents', tags=['incidents'])
bot = HttpTeleBot()


@incidents_router_v1.get('/', response_model=MultipleIncidentResponse)
async def all_incidents(session: SessionDep, pagination: PaginationParams, token: TokenDep):
    logger.debug(f'all incidents: {token.user.id} {pagination}')
    if pagination.limit is None and pagination.skip is None:
        incidents = await DB.incidents.all(session=session, load_relations=True)
    else:
        incidents = await DB.incidents.pagination(
            skip=pagination.skip,
            limit=pagination.limit,
            order_by_field='created_at',
            session=session,
            load_relations=True,
        )

    return {'incidents': [{
        'id': i.id,
        'title': i.title,
        'message': i.message,
        'logs': i.logs,
        'level': i.level,
        'status': i.status,
        'app_name': i.app.name,
        'created_at': i.created_at,
        'updated_at': i.updated_at,
        'edit_by_user': i.edit_by.name if i.edit_by is not None else None
    } for i in incidents]}


@incidents_router_v1.post('/new', response_model=Ok)
async def post_incident(incident: IncidentRequest, app: AppDep, session: SessionDep):
    return {'ok': await DB.incidents.new(
        title=incident.title,
        message=incident.message,
        logs=incident.logs,
        level=incident.level,
        app_id=app.id,
        session=session,
        commit=True
    )}


@incidents_router_v1.get('/{incident_id}', response_model=IncidentResponse)
async def incident_by_id(session: SessionDep, token: TokenDep, incident_id: int):
    inc = await DB.incidents.by_id(incident_id=incident_id, session=session, load_relations=True)
    if inc is None:
        raise HTTPException(status_code=404, detail=f'Incident {incident_id} not found')
    return {
        'title': inc.title,
        'message': inc.message,
        'logs': inc.logs,
        'level': inc.level,
        'status': inc.status,
        'app_name': inc.app.name,
    }


@incidents_router_v1.delete('/{incident_id}', response_model=Ok)
async def del_incident_by_id(session: SessionDep, token: TokenDep, incident_id: int):
    try:
        return {'ok': await DB.incidents.del_by_id(
            incident_id=incident_id,
            session=session,
            commit=True,
        )}
    except ItemNotFound:
        raise HTTPException(status_code=404, detail='Incident not found')


@incidents_router_v1.put('/{incident_id}/status', response_model=Ok)
async def update_status(
    session: SessionDep,
    token: TokenDep,
    incident_id: int,
    status_req: NewStatusRequest
):
    try:
        return {'ok': await DB.incidents.update_status(
            incident_id=incident_id,
            new_status=status_req.new_status,
            updated_by_id=token.user.id,
            session=session,
            commit=True,
        )}
    except ItemNotFound:
        raise HTTPException(status_code=404, detail='Incident not found')
