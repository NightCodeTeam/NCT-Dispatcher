from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from .app import AppDep
from .auth import UserDep
from .db import DBDep
from core.redis_client import RedisDep


@dataclass(frozen=True, slots=True)
class Common:
    user: UserDep
    db: DBDep
    redis: RedisDep


def get_common_dep(user: UserDep, db: DBDep, redis: RedisDep) -> Common:
    return Common(user=user, db=db, redis=redis)


CommonDep = Annotated[Common, Depends(get_common_dep)]


@dataclass(frozen=True, slots=True)
class CommonApp:
    user: UserDep
    db: DBDep
    redis: RedisDep
    app: AppDep


def get_common_app_dep(user: UserDep, db: DBDep, redis: RedisDep, app: AppDep) -> CommonApp:
    return CommonApp(user=user, db=db, redis=redis, app=app)


CommonAppDep = Annotated[CommonApp, Depends(get_common_app_dep)]
