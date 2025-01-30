from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from passlib.context import CryptContext
from config import settings
from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from src.service.exceptions import UserUnauthorized, BadToken


password_context = CryptContext(schemes=[settings.secondary_encode_algorithm], deprecated="auto")


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
        if payload['sub'] and payload['exp']:
            return int(payload['sub'])
        else:
            raise UserUnauthorized()
    except JWTError as e:
        raise UserUnauthorized()


async def get_user_id_from_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            settings.encode_algorithm,
            {'verify_exp': False}
        )
        if payload['sub']:
            return int(payload['sub'])
        else:
            raise BadToken()
    except JWTError as e:
        print(e)
        raise BadToken()


def create_access_token(identity) -> str:
    to_encode = identity.copy()
    expire = datetime.now(UTC) + timedelta(minutes=20)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.encode_algorithm)
    return encoded_jwt


def get_hashed_password(password):
    return password_context.hash(password)


async def verify_password(plain_password, hashed_password):
    return password_context.verify(plain_password, hashed_password)

