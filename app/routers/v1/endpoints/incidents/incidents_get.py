from fastapi import APIRouter
from settings import settings


router = APIRouter(prefix=settings.INCIDENTS_API_PATH)


@router.post('/post_incident')
async def post_incudent():
    pass