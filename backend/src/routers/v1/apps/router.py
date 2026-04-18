
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
    """
    Получение всех приложений.
    """
    return {
        'apps': await AppHandler(common.db).all(
            skip=pagination.skip,
            limit=pagination.limit
        )
    }


@apps_router_v1.post('/new', response_model=Ok)
async def new_app(app: NewAppRequest, common: CommonDep):
    """
    Создание нового приложения.
    Требуются json параметры:
        - name: str - название приложения
        - status_url: str - URL для получения статуса приложения
        - status_code: str | None = None - код доступа для получения данных для приложения
        - logs_folder: str | None = None - папка для хранения логов приложения
        - script_path: str | None = None - путь к скрипту запуска приложения (если оно упало)
    """
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
    """
    Получение данных о приложении по ID.
    """
    app = await common.db.apps.by_id(app_id=app_id)
    if app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='App not found'
        )
    return app


@apps_router_v1.put('/{app_id}', response_model=Ok)
@rate_limiter(max_requests=10, time_delta=30)
async def update_app(app_id: int, new_data: AppUpdateRequest, common: CommonDep):
    """
    Обновление данных о приложении.
    Требуются json параметры:
        - name: str - новое название приложения
        - status_url: str - новый URL для получения статуса приложения
        - status_code: str | None = None - новый код доступа для получения данных для приложения
        - logs_folder: str | None = None - новая папка для хранения логов приложения
        - script_path: str | None = None - новый путь к скрипту запуска приложения (если оно упало)
    """
    app = await common.db.apps.by_id(app_id=app_id)
    if app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='App not found'
        )
    return {'ok': await AppHandler(common.db).update(app=app, new_data=new_data)}


@apps_router_v1.get('/{app_id}/logs', response_model=AppMultipleLogFilesResponse)
@rate_limiter(max_requests=10, time_delta=30)
async def app_logs(app_id: int, common: CommonDep):
    """
    Получение логов приложения по ID.
    """
    app = await common.db.apps.by_id(app_id=app_id)
    if app is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='App not found'
        )

    try:
        return {'logs': await AppHandler(common.db).logs(app=app)}
    except FileNotFoundError:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Logs folder not found'
        )


@apps_router_v1.delete('/{app_id}', response_model=Ok)
async def del_app_by_id(app_id: int, common: CommonDep):
    """
    Удаление приложения по ID.
    """
    try:
        return {'ok': await common.db.apps.del_by_id(app_id=app_id)}
    except ItemNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='App not found'
        )
