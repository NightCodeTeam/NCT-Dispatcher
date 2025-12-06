from typing import Annotated

from fastapi import Depends

from app.core.auth import verify_token, TokenData


Token = Annotated[TokenData, Depends(verify_token)]
