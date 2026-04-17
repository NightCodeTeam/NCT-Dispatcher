import asyncio
import aiohttp
from src.database import DataBase
from src.database.models import App


class AppHandler:
    def __init__(self, db: DataBase):
        self.db = db

    async def get_status(self, app) -> dict:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(app['status_url'], headers={
                    'X-Access-Code': app.get('status_code') or ''
                }) as response:
                    ans = await response.json()
                    return {
                        'id': app['id'],
                        **ans
                    }
        except Exception as e:
            pass
        return {
            'ok': False,
            'cpu_usage': 0,
            'memory_usage': 0,
            'disk_usage': 0,
            'adt_data': None,
            'id': app['id']
        }

    async def all(self, skip: int | None = 0, limit: int | None = 100):
        apps = await self.db.apps.pagination(skip=skip or 0, limit=limit or 100, load_relations=True)
        apps = {i.id: {
        	'id': i.id,
        	'name': i.name,
        	'code': i.code,
            'status_url': i.status_url,
            'status_code': i.status_code,
        	'logs_folder': i.logs_folder,
            'script_path': i.script_path,
        	'incidents_count': len(i.incidents),
        } for i in apps}

        results = await asyncio.gather(*[self.get_status(app) for app in apps.values()])

        for result in results:
            apps[result['id']]['status'] = result

        return tuple(apps.values())

    async def update(
        self,
        app: App,
        new_data,
    ):
        if new_data.status_url is not None:
            app.status_url = new_data.status_url
        if new_data.status_code is not None:
            app.status_code = new_data.status_code
        if new_data.logs_folder is not None:
            app.logs_folder = new_data.logs_folder
        if new_data.script_path is not None:
            app.script_path = new_data.script_path
        if new_data.new_code is True:
            app.code = self.db.apps.generate_code()
        #await self.db.commit()
        return True
