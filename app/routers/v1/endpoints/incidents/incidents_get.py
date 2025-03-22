from fastapi import APIRouter

from routers.v1.models.incidents import IncidentRequest
from fastapi import Request
from database.models.app import App
from sqlalchemy import select
from pydantic import BaseModel

from dependencies.dependencies import SessionDep, AppDep
from settings import settings


router = APIRouter(prefix=settings.INCIDENTS_API_PATH)

class Test(BaseModel):
    app: str
    dispatch: str



@router.post('/test')
async def get_app2(test: Test, request: Request, session: SessionDep):
    print(test)
    #res = await session.execute(select(App))
    res = await session.execute(select(App).where(
        App.name == test.app, #request.headers.get('app'),
        App.dispatcher_code == test.dispatch#request.headers.get('dispatch')
    ))
    if res.first() is not None:
        print(res.first()[0])
    return {'ok'}





@router.post('/post_incident')
async def post_incident(incident: IncidentRequest, app: AppDep, session: SessionDep):
    pass