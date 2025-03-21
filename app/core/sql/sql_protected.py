from dataclasses import is_dataclass, fields
from .sql_exceptions import SQLInjectionException
from .sql_settings import SQL_EXCEPT_CHARS  #, SQL_EXCEPT_VALUES


def parse_arg(string_to_parse: str):
    # ! Берем строку и разбиваем её на буквы, следим чтобы те не были в запрещенных
    if len(string_to_parse) > 1:
        for word in string_to_parse.split(' '):
            if word in SQL_EXCEPT_CHARS:
                raise SQLInjectionException(word, string_to_parse)

    for char in string_to_parse:
        if char in SQL_EXCEPT_CHARS:
            raise SQLInjectionException(char, string_to_parse)


def check_args(args: list | tuple):
    for arg in args:
        if type(arg) is str:
            parse_arg(arg)
        elif is_dataclass(arg):
            for field in fields(arg):
                if field.type == str:
                    parse_arg(getattr(arg, field.name))


def sql_protected_async(func):
    """Принимаем Асинхронную функцию, проверяем чтобы не было опасных вставок"""
    async def wrapped(*args, **kwargs):
        check_args((*args, *kwargs.values()))

        return await func(*args, **kwargs)
    return wrapped


def sql_protected(func):
    """Принимаем синхронную функцию, проверяем чтобы не было опасных вставок"""
    def wrapped(*args, **kwargs):
        check_args((*args, *kwargs.values()))

        return func(*args, **kwargs)
    return wrapped