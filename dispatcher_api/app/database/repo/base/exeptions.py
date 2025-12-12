from typing import Type

from .classes import T


class RepositoryException(Exception):
    pass


class ItemNotFound(RepositoryException):
    def __init__(self, model: Type[T], search_field: str, search_value: str | int):
        super().__init__(f'Item not found: {model}.{search_field} = {search_value}')
