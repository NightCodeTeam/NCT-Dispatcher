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


def get_common_dep(user: UserDep, db: DBDep) -> Common:
    return Common(user=user, db=db)


CommonDep = Annotated[Common, Depends(get_common_dep)]


@dataclass(frozen=True, slots=True)
class CommonApp:
    user: UserDep
    db: DBDep
    app: AppDep


def get_common_app_dep(user: UserDep, db: DBDep, xapp: AppDep) -> CommonApp:
    return CommonApp(user=user, db=db, app=app)


CommonAppDep = Annotated[CommonApp, Depends(get_common_app_dep)]
