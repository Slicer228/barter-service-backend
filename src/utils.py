import logging, asyncio
from fastapi import Request, Depends
from jose import JWTError, jwt
from config import settings
from src.exceptions import UserUnauthorized
from datetime import datetime, UTC

logging.basicConfig(level=logging.ERROR,filename="logs.log",filemode="a",
format="%(asctime)s %(levelname)s %(message)s"
)

async def addLog(err):
    logging.error(str(err))

async def get_token(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        raise UserUnauthorized()
    else:
        return token

async def get_user_from_token(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            settings.encode_algorithm
        )
        print(payload)
        if payload['sub'] and payload['exp']:
            return int(payload['sub'])
        else:
            raise UserUnauthorized()
    except JWTError:
        raise UserUnauthorized()
