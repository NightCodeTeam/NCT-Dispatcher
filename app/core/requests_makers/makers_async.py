import aiohttp
import asyncio
from core.debug import create_log
from .makers_exceptions import RequestMethodNotFoundException
from .requests_dataclasses import ResponseData, Method
from ..single import Singleton


class HttpMakerAsync(Singleton):
    __session: aiohttp.ClientSession

    def __init__(self, base_url: str, headers: dict | None = None):
        self._base_url = base_url
        self._headers = headers
        self.__session = aiohttp.ClientSession(base_url=base_url, headers=headers)
        # Если инициализировать класс до асинхронного кода вылетит ошибка создания сессии

    def __del__(self):
        loop = asyncio.new_event_loop()
        loop.create_task(self.close_session())
        #self.__session = None
        #self.close_session_sync()

    def close_session_sync(self):
        if not self.__session.closed:
            try:
                loop = asyncio.get_event_loop()
                if loop is not None:
                    #asyncio.ensure_future(self.close_session(), loop=loop)
                    loop.create_task(self.close_session())
            except RuntimeError as error:
                print(f'>>>>>> {error}')
                loop = asyncio.new_event_loop()
                loop.create_task(self.close_session())
                #asyncio.run(self.close_session())

    async def close_session(self):
        await self.__session.close()
        create_log(f'{type(self).__name__} > session closed', 'info')

    async def _make(
            self,
            url: str,
            method: Method,
            data: dict | None = None,
            json: dict | None = None,
            params: dict | None = None,
            headers: dict | None = None,
    ) -> ResponseData | None:
        try:
            res = None
            # Убрана часть с кэшем она тут не нужна
            # ! Делаем запрос
            match method:
                case 'GET':
                    res = await self.__session.get(
                        url=url,
                        data=data,
                        json=json,
                        params=params,
                        headers=headers
                    )
                case 'POST':
                    res = await self.__session.post(
                        url=url,
                        data=data,
                        json=json,
                        params=params,
                        headers=headers
                    )
                case 'PUT':
                    res = await self.__session.put(
                        url=url,
                        data=data,
                        json=json,
                        params=params,
                        headers=headers
                    )
                case 'DELETE':
                    res = await self.__session.delete(
                        url=url,
                        data=data,
                        json=json,
                        params=params,
                        headers=headers
                    )
            if res is not None:
                return await self.__get_response_data(res)
            raise RequestMethodNotFoundException(method)
        except aiohttp.ClientConnectorError:
            return None

    @staticmethod
    async def __get_response_data(response: aiohttp.ClientResponse) -> ResponseData:
        try:
            data = await response.json()
            if type(data) is not dict:
                data = {'data': data}
        except aiohttp.ContentTypeError as e:
            create_log(e, 'error')
            data = {'error': await response.text()}
        return ResponseData(
            response.status,
            data
        )
