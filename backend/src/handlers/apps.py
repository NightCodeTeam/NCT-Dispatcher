import asyncio
import aiohttp
from src.database import DataBase


class AppHandler:
    def __init__(self, db: DataBase):
        self.db = db

    async def get_status(self, app) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(app.status_url) as response:
                try:
                    ans = await response.json()
                    return {
                        'id': app.id,
                        **ans
                    }
                except Exception as e:
                    pass
                return {
                    'ok': False,
                    'id': app.id
                }

    async def all_apps(self, skip: int = 0, limit: int = 100):
        apps = await self.db.apps.pagination(skip=skip, limit=limit, load_relations=True)
        apps = {app.id: app.model_dump() for app in apps}

        results = await asyncio.gather(*[self.get_status(app) for app in apps.values()])

        for result in results:
            apps[result['id']].update(result)

        return apps
