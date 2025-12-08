from fastapi import APIRouter

from depends import SessionDep, AppDep, TokenDep, PaginationParams
from database import DB
from routers.misc_models import Ok
from bot_tele.bot_requests import HttpTeleBot
from .models import IncidentRequest, MultipleIncidentResponse, IncidentResponse
from .models import NewStatusRequest


incidents_router_v1 = APIRouter(prefix='/incidents', tags=['incidents'])
bot = HttpTeleBot()


@incidents_router_v1.get('/', response_model=MultipleIncidentResponse)
async def all_incidents(session: SessionDep, pagination: PaginationParams, token: TokenDep):
    if pagination.limit is None and pagination.skip is None:
        return {'incidents': await DB.incidents.all(session=session, load_relations=False)}
    return {'incidents': await DB.incidents.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        session=session,
        load_relations=False,
    )}


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
    return await DB.incidents.by_id(incident_id=incident_id, session=session)


@incidents_router_v1.delete('/{incident_id}', response_model=Ok)
async def del_incident_by_id(session: SessionDep, token: TokenDep, incident_id: int):
    return await DB.incidents.del_by_id(
        incident_id=incident_id,
        session=session,
        commit=True,
    )


@incidents_router_v1.put('/{incident_id}/status', response_model=Ok)
async def update_status(
    session: SessionDep,
    token: TokenDep,
    incident_id: int,
    status_req: NewStatusRequest
):
    return {'ok': await DB.incidents.update_status(
        incident_id=incident_id,
        new_status=status_req.new_status,
        session=session,
        commit=True,
    )}
