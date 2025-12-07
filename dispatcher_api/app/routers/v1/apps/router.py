from fastapi import APIRouter

from depends import SessionDep, Token, PaginationParams
from database import DB
from routers.misc_models import Ok
from .models import NewAppRequest, AppResponse, MultipleAppsResponse


apps_router_v1 = APIRouter(prefix='/apps', tags=['apps'])


@apps_router_v1.post('/new', response_model=Ok)
async def new_app(app: NewAppRequest, session: SessionDep, token: Token):
    return {'ok': await DB.apps.new(
        name=app.name,
        status_url=app.status_url,
        logs_folder=app.logs_folder,
        added_by=token.user.id,
        session=session
    )}


@apps_router_v1.get('/', response_model=MultipleAppsResponse)
async def all_apps(session: SessionDep, pagination: PaginationParams, token: Token):
    if pagination.limit is None and pagination.skip is None:
        return {'apps': await DB.apps.all(session=session, load_relations=False)}
    return {'apps': await DB.apps.pagination(
        skip=pagination.skip,
        limit=pagination.limit,
        session=session,
        load_relations=False,
    )}


@apps_router_v1.get('/{app_id}', response_model=AppResponse)
async def app_by_id(session: SessionDep, token: Token, app_id: int):
    return await DB.apps.by_id(app_id=app_id, session=session)


@apps_router_v1.delete('/{app_id}', response_model=Ok)
async def del_app_by_id(session: SessionDep, token: Token, app_id: int):
    return {'ok': await DB.apps.del_by_id(app_id=app_id, session=session)}


@apps_router_v1.get('/{app_id}/logs')
async def app_logs(session: SessionDep, token: Token, app_id: int):
    ...
