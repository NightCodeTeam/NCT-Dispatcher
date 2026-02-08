from typing import Annotated

from fastapi import Depends, Request, Response

from app.handlers.auth import AuthHandler, User


async def verify_access_token(request: Request, response: Response) -> User:
    return await AuthHandler().verify_token(request, response)


UserDep = Annotated[User, Depends(verify_access_token)]
