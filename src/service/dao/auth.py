from sqlalchemy import update, select
from src.service.db import async_session_maker
from src.models.db import Users
from src.service.exceptions import UserNotFound, UserUnauthorized


async def set_refresh_token(user_id: int, refresh_token: str):
    async with async_session_maker() as session:
        stmt = update(Users).where(Users.user_id == user_id).values(refresh_token=refresh_token)
        await session.execute(stmt)


async def check_refresh_token(user_id: int, refresh_token: str):
    async with async_session_maker() as session:
        stmt = select(Users).where(Users.user_id == user_id)

        data = await session.execute(stmt)
        data = data.scalars().first()

        if data is None:
            raise UserNotFound
        elif data.refresh_token != refresh_token:
            raise UserUnauthorized
