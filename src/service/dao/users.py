from src.schemas.request_s import SchemaAddUser, SchemaAuthUser
from sqlalchemy import select, insert, column
from src.models.dbModels import Users
from src.db import async_session_maker
from src.service.dto.users import userview
from src.service.auth import get_hashed_password, verify_password
from src.internal_exceptions import NotFound, AuthError
import json
from src.exception_handlers import error_handler_users


class User:

    @staticmethod
    @userview
    async def set(usrobj: SchemaAddUser) -> int:
        password = get_hashed_password(usrobj.password)
        stmt = insert(Users).values(username=usrobj.username,
                                    password=password,
                                    avatar=bytes(json.dumps(usrobj.avatar),'utf8'),
                                    email=usrobj.email
                                    )
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    result = await session.execute(stmt)
                    await session.commit()
                    return result.lastrowid
                except BaseException as e:
                    await session.rollback()
                    raise e

    @staticmethod
    @error_handler_users
    async def auth(user: SchemaAuthUser) -> int:
        async with async_session_maker() as session:
            stmt = select(Users).where(Users.email == user.email)
            data = await session.execute(stmt)
            data = data.scalars().first()
            if verify_password(user.password, data.password):
                return data.user_id
            else:
                raise AuthError()

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
                    raise NotFound()

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
