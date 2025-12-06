import random
import string
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import wraps
from time import time

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.debug import logger
from app.database.models import User
from app.database.repo import DB
from app.settings import settings


@dataclass(frozen=True, slots=True)
class TokenData:
    user: User
    exp: int


security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_hashed(plain: str, saved: str):
    return pwd_context.verify(plain, saved)


def unhash(hash_to_str: str):
    return pwd_context.encrypt(hash_to_str)


def get_hash(str_to_hash: str):
    return pwd_context.hash(str_to_hash)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.AUTH_TOKEN_LIFETIME_IN_MIN)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.AUTH_SECRET_KEY, algorithm=settings.AUTH_ALGORITHM)
    return token


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    token = credentials.credentials
    try:
        data = jwt.decode(token, settings.AUTH_SECRET_KEY, algorithms=[settings.AUTH_ALGORITHM])
        if data['exp'] < time():
            logger.log(f'verify_token > expired for {data['sub']}', 'info')
            raise JWTError

        user = await DB.users.by_name(data['sub'])
        if user is None:
            logger.log(f'verify_token > {data['sub']} not exists', 'info')
            raise JWTError

        return TokenData(user=user, exp=data['exp'])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
