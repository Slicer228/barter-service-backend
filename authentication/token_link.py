from datetime import datetime, UTC, timedelta
from authentication.auth import password_context
from typing import Dict
from src.service.exceptions import UserUnauthorized, BadToken


def generate_refresh_token(access_token: str) -> Dict[str, str]:
    sign = access_token[::-1][:12]
    expires_in = 60 * 60 * 24 * 365
    expires_at = datetime.now(UTC) + timedelta(seconds=expires_in)

    rt = {"exp": expires_at}
    hashed_sign = password_context.hash(sign)
    rt.update({"token": hashed_sign})

    return rt


def check_rt_expired(refresh_token: dict):
    if datetime.now(UTC) > datetime.fromtimestamp(float(refresh_token.get('exp'))):
        raise BadToken()
    return refresh_token


def verify_refresh_token(token: str, rt: str):
    sign = token[::-1][:12]
    if not password_context.verify(sign, rt):
        raise BadToken()
