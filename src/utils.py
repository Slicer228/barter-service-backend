import logging,asyncio
from fastapi import Request, HTTPException, Depends
from src.routers.responses import UserResponse
from jose import JWTError, jwt
from config import settings
from src.errors import AuthError
from datetime import datetime, UTC

logging.basicConfig(level=logging.ERROR,filename="logs.log",filemode="a",
format="%(asctime)s %(levelname)s %(message)s"
)

async def addLog(err):
    logging.error(str(err))

async def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(**UserResponse.NOT_AUTH)
    else:
        return token

async def get_user_from_token(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            settings.encode_algorithm
        )
        if payload['sub'] and payload['exp']:
            return int(payload['sub'])
        else:
            raise HTTPException(**UserResponse.NOT_AUTH)
    except JWTError:
        raise HTTPException(**UserResponse.NOT_AUTH)
