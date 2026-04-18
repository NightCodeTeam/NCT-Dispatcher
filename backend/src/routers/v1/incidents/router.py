from fastapi import APIRouter, HTTPException

from core.pydantic_misc_models import Ok
from core.fast_decorators import cache, rate_limiter
from core.redis_client import RedisDep
from core.fast_depends import PaginationParams
from core.sql_repository import ItemNotFound
from src.depends import UserDep, DBDep, AppDep, CommonDep
from src.services.authservice import AuthService
from src.handlers import IncidentsHandler
from .models import IncidentRequest, MultipleIncidentResponse, IncidentResponse
from .models import NewStatusRequest


incidents_router_v1 = APIRouter(prefix='/v1/incidents', tags=['incidents'])


@incidents_router_v1.get('', response_model=MultipleIncidentResponse)
@cache(key='incidents:all_incident')
@rate_limiter(max_requests=10, time_delta=30)
async def all_incidents(pagination: PaginationParams, common: CommonDep, redis: RedisDep):
    """
    Получение всех инцидентов. Рекомендуется использовать параметрами пагинации.
    """
    return {'incidents': await IncidentsHandler(common.db).all(
        redis=redis,
        skip=pagination.skip,
        limit=pagination.limit,
    )}


@incidents_router_v1.post('/new', response_model=Ok)
async def post_incident(incident: IncidentRequest, app: AppDep, db: DBDep):
    """
    Создание нового инцидента. Вам потребуется:
        - 'incident' - данные об инциденте
            - 'title' - заголовок инцидента
            - 'message' - сообщение об инциденте
            - 'logs' - логи инцидента
            - 'level' - уровень инцидента
        - 'app_name' - имя приложения (сохраненное в dispatcher)
        - 'app_code' - код приложения (выдется при создании приложения)
    """
    return {'ok': await db.incidents.new(
        title=incident.title,
        message=incident.message,
        logs=incident.logs,
        level=incident.level,
        app_id=app.id,
        commit=False
    )}


@incidents_router_v1.get('/{incident_id}', response_model=IncidentResponse)
@cache(key='incidents:by_id')
@rate_limiter(max_requests=10, time_delta=30)
async def incident_by_id(incident_id: int, common: CommonDep, redis: RedisDep):
    """
    Получение информации об инциденте по ID.
    """
    inc = await common.db.incidents.by_id(incident_id=incident_id, load_relations=True)
    if inc is None:
        raise HTTPException(status_code=404, detail=f'Incident {incident_id} not found')
    return await IncidentsHandler(common.db).by_id(incident=inc, redis=redis)


@incidents_router_v1.delete('/{incident_id}', response_model=Ok)
async def del_incident_by_id(db: DBDep, user: UserDep, incident_id: int):
    """
    Удаление инцидента по ID.
    """
    try:
        return {'ok': await db.incidents.del_by_id(
            incident_id=incident_id,
            commit=True,
        )}
    except ItemNotFound:
        raise HTTPException(status_code=404, detail='Incident not found')


@incidents_router_v1.put('/{incident_id}/status', response_model=Ok)
async def update_status(
    common: CommonDep,
    incident_id: int,
    status_req: NewStatusRequest
):
    """
    Обновление статуса инцидента открыт/закрыт.
    """
    try:
        return {'ok': await common.db.incidents.update_status(
            incident_id=incident_id,
            new_status=status_req.new_status,
            updated_by_id=common.user.id,
        )}
    except ItemNotFound:
        raise HTTPException(status_code=404, detail='Incident not found')
