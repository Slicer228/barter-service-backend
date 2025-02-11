from src.models.db import Users
from src.schemas.request import RegisterUserSchema
from src.service.core.users import dao


async def get_user(user_id: int):
    return await dao.get_user(user_id)


async def set_refresh_token(user_id: int, refresh_token: dict):
    return await dao.set_refresh_token(user_id, refresh_token)


async def check_rt_and_get_exp(user_id: int, refresh_token: str):
    return await dao.check_rt_and_get_exp(user_id, refresh_token)


async def get_user_from_email(email: str) -> Users:
    return await dao.get_user_from_email(email)


async def register_user(usrobj: RegisterUserSchema) -> int:
    return await dao.register_user(usrobj)
