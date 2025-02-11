from src.schemas.request import RegisterUserSchema
from sqlalchemy import select, insert, update
from src.models.db import Users, EmailVerification
from src.service.db import async_session_maker
from src.service.dto.users import userview
from src.authentication.auth import get_hashed_password
from src.exc.exceptions import UserNotFound, BadToken
import json
from src.service.core.utils_dao import email_exists
from datetime import datetime


class User:

    @classmethod
    async def set(cls, usrobj: RegisterUserSchema) -> int:
        password = get_hashed_password(usrobj.password)

        async with async_session_maker() as session:

            async with session.begin():
                try:
                    await email_exists(session, usrobj.email)

                    stmt = insert(EmailVerification).values(email=usrobj.email)
                    await session.execute(stmt)
                    stmt = insert(Users).values(username=usrobj.username,
                                                password=password,
                                                avatar=bytes(json.dumps(usrobj.avatar), 'utf8'),
                                                email=usrobj.email
                                                )
                    result = await session.execute(stmt)
                    await session.commit()
                    return result.lastrowid
                except BaseException as e:
                    print(e)
                    await session.rollback()
                    raise e

    @staticmethod
    async def get_user_from_email(email: str) -> Users:
        async with async_session_maker() as session:
            stmt = select(Users).where(Users.email == email)
            result = await session.execute(stmt)
            result = result.scalars().first()
            if result:
                return result
            else:
                raise UserNotFound()

    @staticmethod
    async def check_rt_and_get_exp(user_id: int, refresh_token: str):
        async with async_session_maker() as session:
            stmt = select(Users).where(Users.user_id == user_id)

            data = await session.execute(stmt)
            data = data.scalars().first()

            rt = json.loads(data.refresh_token)

            if rt.get('token') != refresh_token:
                raise BadToken()

            if not data:
                raise BadToken()

            return datetime.fromisoformat(rt.get('exp'))

    @staticmethod
    async def set_refresh_token(user_id: int, refresh_token: dict):
        async with async_session_maker() as session:
            stmt = update(Users).where(Users.user_id == user_id).values(
                refresh_token=json.dumps(refresh_token, default=datetime.isoformat)
            )

            await session.execute(stmt)
            await session.commit()

    @staticmethod
    @userview
    async def get_user(user_id: int | list[int]) -> list[Users]:
        async with async_session_maker() as session:
            if isinstance(user_id, list):
                users = []
                for user in user_id:
                    stmt = select(Users).where(Users.user_id == user)
                    result = await session.execute(stmt)
                    result = result.scalars().first()
                    users.append(result)
                return users
            else:
                stmt = select(Users).where(Users.user_id == user_id)
                result = await session.execute(stmt)
                result = result.scalars().first()
                if result:
                    return [result]
                else:
                    raise UserNotFound()

    @staticmethod
    @userview
    async def add_green_points(user_id: int, gp: int):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                except BaseException as e:
                    await session.rollback()
                    raise e

    @staticmethod
    @userview
    async def refactor_green_score(user_id: int, isGoodBoy: bool = False):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                except BaseException as e:
                    await session.rollback()
                    raise e

    @staticmethod
    @userview
    async def rename(user_id: int, new_name: str):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                except BaseException as e:
                    await session.rollback()
                    raise e

    @staticmethod
    @userview
    async def update_photo(user_id: int, new_photo):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                except BaseException as e:
                    await session.rollback()
                    raise e

    @staticmethod
    @userview
    async def update_password(user_id: int, new_password: str):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                except BaseException as e:
                    await session.rollback()
                    raise e