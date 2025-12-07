from fastapi import APIRouter

from depends import SessionDep, Token, PaginationParams
from database import DB
from routers.misc_models import Ok
from .models import NewAppRequest, AppResponse, MultipleAppsResponse

apps_router_v1 = APIRouter(prefix='/apps', tags=['apps'])


@apps_router_v1.post('/new', response_model=Ok)
async def new_app(app: NewAppRequest, session: SessionDep, token: Token):
    pass


@apps_router_v1.get('/', response_model=MultipleAppsResponse)
async def all_apps(session: SessionDep, pagination: PaginationParams, token: Token):
    pass


@apps_router_v1.get('/{app_id}', response_model=AppResponse)
async def app_by_id(session: SessionDep, token: Token, app_id: int):
    pass


@apps_router_v1.delete('/{app_id}', response_model=Ok)
async def del_app_by_id(session: SessionDep, token: Token, app_id: int):
    pass
