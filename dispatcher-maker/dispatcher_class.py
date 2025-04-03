import logging
import requests
from typing import Literal

Level = Literal['debug', 'warning', 'info', 'error', 'crit']


class Dispatcher:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, dispatcher_url: str, dispatcher_code: str, app_name: str):
        self.__dispatcher_url = dispatcher_url
        self.__dispatcher_code = dispatcher_code
        self.__app_name = app_name

    def sent(self, title: str, message: str, level: Level, logs: str | list[str] | tuple[str]):
        if type(logs) is list or type(logs) is tuple:
            logs='\n'.join(logs)
        res = requests.post(
            self.__dispatcher_url,
            json={
                'title': title,
                'message': message,
                'level': level,
                'logs': logs,
                'app_name': self.__app_name,
            }, headers={
                'Content-Type': 'application/json',
                'dispatch': self.__dispatcher_code,
            }
        )


