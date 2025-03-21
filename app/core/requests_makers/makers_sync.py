import requests

from .requests_dataclasses import ResponseData, Method, AllowedMethods
from .makers_exceptions import RequestMethodNotFoundException
from .makers_cache import CacheMaker
from ..debug import create_log
from ..single import Singleton


class HttpMaker(Singleton):
    _session: requests.Session

    def __init__(
        self,
        base_url: str = '',
        headers = None | dict,
        make_cache: bool = True,
        cache_class: CacheMaker | None = None
    ):
        if headers is None:
            headers = dict()
        self.base_url = base_url if base_url.endswith('/') else f'{base_url}/'
        self.headers = headers
        self.make_cache = make_cache
        self.cache = cache_class

    def get_full_path(self, url) -> str:
        return f'{self.base_url}{url}'

    def __execute(
            self,
            url: str,
            method: Method,
            data: dict | None = None,
            json: dict | None = None,
            params: dict | None = None,
            headers: dict | None = None,
    ) -> ResponseData | None:
        try:
            headers.update(self.headers) if headers is not None and self.headers is not None else self.headers
            with requests.Session() as session:
                if method.upper() in AllowedMethods:
                    return self._get_response_data(getattr(session, method.lower())(
                        url=self.get_full_path(url),
                        data=data,
                        json=json,
                        params=params,
                        headers=headers
                    ))
                else:
                    raise RequestMethodNotFoundException(method)
        except requests.exceptions.ConnectionError as e:
            create_log(e, 'error')
        except requests.exceptions.RequestException as e:
            create_log(e, 'error')
        except AttributeError as e:
            create_log(e, 'crit')

    def _make(
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

        res = self.__execute(
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
    def _get_response_data(response: requests.Response) -> ResponseData:
        try:
            data = response.json()
            if type(data) is not dict:
                data = {'data': data}
        except (
            requests.exceptions.ContentDecodingError,
            requests.exceptions.JSONDecodeError
        ) as e:
            data = {'error': response.text}
            create_log(e, 'error')
        return ResponseData(
            url=response.url,
            status=response.status_code,
            headers=response.headers,
            json=data,
        )
