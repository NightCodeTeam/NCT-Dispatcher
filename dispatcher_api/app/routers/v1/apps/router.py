from os import listdir

from fastapi import APIRouter, HTTPException, status

from depends import SessionDep, PaginationParams, TokenDep
from database import DB
from database.repo.base import ItemNotFound
from routers.misc_models import Ok
from .models import NewAppRequest, MultipleAppsResponse, AppMultipleLogFilesResponse, AppResponse

apps_router_v1 = APIRouter(prefix='/v1/apps', tags=['apps'])


@apps_router_v1.get('/', response_model=MultipleAppsResponse)
async def all_apps(session: SessionDep, pagination: PaginationParams, token: TokenDep):
    if pagination.limit is None and pagination.skip is None:
        apps = await DB.apps.all(session=session, load_relations=True)
    else:
        apps = await DB.apps.pagination(
            skip=pagination.skip,
            limit=pagination.limit,
            session=session,
            load_relations=True,
        )
    return {'apps': apps}


@apps_router_v1.post('/new', response_model=Ok)
async def new_app(app: NewAppRequest, session: SessionDep, token: TokenDep):
    return {'ok': await DB.apps.new(
        name=app.name,
        status_url=app.status_url,
        logs_folder=app.logs_folder,
        added_by_id=token.user.id,
        session=session
    )}


@apps_router_v1.get('/{app_id}', response_model=AppResponse)
async def app_by_id(session: SessionDep, app_id: int, token: TokenDep):
    app = await DB.apps.by_id(app_id=app_id, session=session)
    if app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='App not found'
        )
    return app


@apps_router_v1.get('/{app_id}/logs', response_model=AppMultipleLogFilesResponse)
async def app_logs(session: SessionDep, app_id: int, token: TokenDep):
    app = await DB.apps.by_id(app_id=app_id, session=session)
    if app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='App not found'
        )

    logs = []
    try:
        for file_path in listdir(app.logs_folder):
            with open(f'{app.logs_folder}/{file_path}', 'r') as f:
                logs.append({
                    'title': file_path,
                    'log': f.read()
                })
        return {'logs': logs}
    except FileNotFoundError:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Logs folder not found'
        )


@apps_router_v1.delete('/{app_id}', response_model=Ok)
async def del_app_by_id(session: SessionDep, app_id: int, token: TokenDep):
    try:
        return {'ok': await DB.apps.del_by_id(app_id=app_id, session=session)}
    except ItemNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='App not found'
        )
