import asyncio

import aiohttp
from .requests_dataclasses import ResponseData, Method, AllowedMethods
from .makers_exceptions import RequestMethodNotFoundException
from .makers_cache import CacheMaker
from ..debug import create_log
from ..single import Singleton


class HttpMakerAsync(Singleton):
    def __init__(
        self,
        base_url: str = '',
        headers: None | dict = None,
        make_cache: bool = True,
        cache_class: CacheMaker | None = None
    ):
        if headers is None:
            headers = dict()
        self._base_url = base_url if base_url.endswith('/') else f'{base_url}/'
        self._headers = headers
        self.make_cache = make_cache
        self.cache = cache_class

    def get_full_path(self, url) -> str:
        return f'{self._base_url}{url}'

    async def __execute(
            self,
            url: str,
            method: Method,
            data: dict | None = None,
            json: dict | None = None,
            params: dict | None = None,
            headers: dict | None = None,
    ) -> ResponseData | None:
        res = None
        try:
            async with aiohttp.ClientSession() as session:
                match method.upper():
                    case 'GET':
                        res = await session.get(
                            url=self.get_full_path(url),
                            data=data,
                            json=json,
                            params=params,
                            headers=headers
                        )
            return await self.__get_response_data(res)
            #print(self._base_url)
            #async with aiohttp.ClientSession(base_url=self._base_url, headers=self._headers) as session:
            #    if method.upper() in AllowedMethods:
            #        return await self.__get_response_data(await (getattr(session, method.lower())(
            #        )))
            #    else:
            #        raise RequestMethodNotFoundException(method)
        except aiohttp.ClientConnectorError as e:
            create_log(e, 'error')
        except aiohttp.ConnectionTimeoutError as e:
            if res is not None:
                create_log(await self.__get_response_data(res), 'error')
            create_log(e, 'error')
            await asyncio.sleep(60)
        except AttributeError as e:
            create_log(e, 'crit')

    async def _make(
            self,
            url: str,
            method: Method,
            data: dict | None = None,
            json: dict | None = None,
            params: dict | None = None,
            headers: dict | None = None,
            try_only_cache: bool = False
    ) -> ResponseData | None:
        url = url if not url.startswith('/') else url[1:]
        if self.cache is not None:
            # ! Пытаемся получить кэш по url
            cache_data = self.cache.get(self.get_full_path(url))
            if cache_data is not None:
                # ? Если возвращать только кэш или выполняется условие кэша
                if try_only_cache or self.cache.condition(cache_data):
                    return cache_data

        res = await self.__execute(
            url=url,
            method=method,
            data=data,
            json=json,
            params=params,
            headers=headers
        )

        if self.cache is not None and res is not None:
            # ! Сохраняем кэш
            if self.make_cache:
                self.cache.put(res)

        return res

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
            url=response.url,
            status=response.status,
            headers=response.headers,
            json=data,
        )
