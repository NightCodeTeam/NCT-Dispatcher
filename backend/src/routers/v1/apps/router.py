from os import listdir

from fastapi import APIRouter, HTTPException, status

from core.pydantic_misc_models import Ok
from core.fast_decorators import cache, rate_limiter
from core.redis_client import RedisDep
from core.fast_depends import PaginationParams
from core.sql_repository import ItemNotFound
from src.depends import DBDep, UserDep, CommonDep
from src.handlers.apps import AppHandler
from .models import (
    NewAppRequest,
    MultipleAppsResponse,
    AppMultipleLogFilesResponse,
    AppResponse,
    AppUpdateRequest,
)


apps_router_v1 = APIRouter(prefix='/v1/apps', tags=['apps'])


@apps_router_v1.get('', response_model=MultipleAppsResponse)
@cache(key='apps:all')
@rate_limiter(max_requests=10, time_delta=30)
async def all_apps(pagination: PaginationParams, common: CommonDep, redis: RedisDep):
    return {'apps': await AppHandler(common.db).all(skip=pagination.skip, limit=pagination.limit)}


@apps_router_v1.post('/new', response_model=Ok)
async def new_app(app: NewAppRequest, common: CommonDep):
    return {'ok': await common.db.apps.new(
        name=app.name,
        status_url=app.status_url,
        status_code=app.status_code,
        logs_folder=app.logs_folder,
        script_path=app.script_path,
        added_by_id=common.user.id,
    )}


@apps_router_v1.get('/{app_id}', response_model=AppResponse)
@cache(key='apps:by_id')
@rate_limiter(max_requests=10, time_delta=30)
async def app_by_id(app_id: int, common: CommonDep, redis: RedisDep):
    app = await common.db.apps.by_id(app_id=app_id)
    if app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='App not found'
        )
    return app


@apps_router_v1.put('/{app_id}', response_model=Ok)
@rate_limiter(max_requests=10, time_delta=30)
async def app_by_id(app_id: int, new_data: AppUpdateRequest, common: CommonDep):
    app = await common.db.apps.by_id(app_id=app_id)
    if app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='App not found'
        )
    return {'ok': await AppHandler.update(app=app, new_data=new_data)}


@apps_router_v1.get('/{app_id}/logs', response_model=AppMultipleLogFilesResponse)
@rate_limiter(max_requests=10, time_delta=30)
async def app_logs(app_id: int, common: CommonDep):
    app = await common.db.apps.by_id(app_id=app_id)
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
async def del_app_by_id(db: DBDep, app_id: int, user: UserDep):
    try:
        return {'ok': await db.apps.del_by_id(app_id=app_id)}
    except ItemNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='App not found'
        )
