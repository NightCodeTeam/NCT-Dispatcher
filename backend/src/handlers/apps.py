import asyncio
from os import listdir

import aiohttp
from src.database import DataBase
from src.database.models import App


class AppHandler:
    """
    Обработчик для работы с приложениями.
    """
    def __init__(self, db: DataBase):
        self.db = db

    async def get_status(self, app) -> dict:
        """
        Получает статус приложения.
        """
        try:
            if not app['status_url'].startswith('http'):
                raise ValueError("status_url is None")
            async with aiohttp.ClientSession() as session:
                async with session.get(app['status_url'], headers={
                    'X-Access-Code': app.get('status_code') or ''
                }) as response:
                    ans = await response.json()
                    return {
                        'id': app['id'],
                        **ans
                    }
        except Exception:
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
        """
        Получает список всех приложений с их статусами.
        """
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

    async def by_id(self, app_id: int) -> dict | None:
        """
        Получает приложение по его ID.
        """
        app = await self.db.apps.by_id(app_id, load_relations=True)
        if app is None:
            return None
        app = {
            'id': app.id,
            'name': app.name,
            'code': app.code,
            'status_url': app.status_url,
            'status_code': app.status_code,
            'logs_folder': app.logs_folder,
            'script_path': app.script_path,
            'incidents_count': len(app.incidents),
        }
        app['status'] = await self.get_status(app)
        return app

    async def update(
        self,
        app: App,
        new_data,
    ):
        """
        Обновляет данные приложения.
        """
        if new_data.status_url is not None:
            app.status_url = new_data.status_url
        if new_data.status_code is not None:
            app.status_code = new_data.status_code
        if new_data.logs_folder is not None:
            app.logs_folder = new_data.logs_folder
        if new_data.script_path is not None:
            app.script_path = new_data.script_path
        if new_data.new_code:
            app.code = self.db.apps.generate_code()
        #await self.db.commit()
        return True

    async def logs(self, app: App) -> tuple[dict]:
        """
        Получает логи приложения.
        """
        logs = []
        for file_path in listdir(app.logs_folder):
            with open(f'{app.logs_folder}/{file_path}', 'r') as f:
                logs.append({
                    'title': file_path,
                    'log': f.read()
                })
        return tuple(logs)
