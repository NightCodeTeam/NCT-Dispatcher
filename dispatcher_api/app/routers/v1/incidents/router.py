import logging

from fastapi import APIRouter

from depends import SessionDep, AppDep, Token, PaginationParams
from database.models import Incident
from database import DB
from routers.misc_models import Ok
from bot_tele.bot_requests import HttpTeleBot
from .models import IncidentRequest, MultipleIncidentResponse, IncidentResponse

incidents_router_v1 = APIRouter(prefix='/incidents', tags=['incidents'])
bot = HttpTeleBot()


@incidents_router_v1.post('/new', response_model=Ok)
async def post_incident(incident: IncidentRequest, app: AppDep, session: SessionDep):
    pass


@incidents_router_v1.get('/', response_model=MultipleIncidentResponse)
async def all_incidents(session: SessionDep, pagination: PaginationParams, token: Token):
    pass


@incidents_router_v1.get('/{incident_id}', response_model=IncidentResponse)
async def incident_by_id(session: SessionDep, token: Token, incident_id: int):
    pass


@incidents_router_v1.delete('/{incident_id}', response_model=Ok)
async def del_incident_by_id(session: SessionDep, token: Token, incident_id: int):
    pass
