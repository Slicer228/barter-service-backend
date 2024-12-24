import json
from sqlalchemy.exc import IntegrityError, DBAPIError
from src.models.paramClasses import SchemaAddUser
from sqlalchemy import select, insert
from src.models.dbModels import Users
from src.db import async_session_maker
from src.service.dto.users import userview
from src.service.auth import get_hashed_password
from src.routers.responses import UserResponse
from src.errors import NotFound

class User:

    @staticmethod
    @userview
    async def set(usrobj: SchemaAddUser):
        password = get_hashed_password(usrobj.password)
        stmt = insert(Users).values(username=usrobj.username,password=password, avatar=bytes(json.dumps(usrobj.avatar),'utf8'), email=usrobj.email)
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    result = await session.execute(stmt)
                    await session.commit()
                finally:
                    await session.rollback()

    @staticmethod
    @userview
    async def get_user(user_id: int):
        stmt = select(Users).where(Users.user_id == user_id)
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            result = result.scalars().first()
            if result:
                return result
            else:
                raise NotFound()

    @staticmethod
    @userview
    async def add_green_points(user_id: int, gp: int):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                finally:
                    await session.rollback()

    @staticmethod
    @userview
    async def refactor_green_score(user_id: int, isGoodBoy: bool = False):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                finally:
                    await session.rollback()

    @staticmethod
    @userview
    async def rename(user_id: int, new_name: str):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                finally:
                    await session.rollback()

    @staticmethod
    @userview
    async def update_photo(user_id: int, new_photo):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                finally:
                    await session.rollback()

    @staticmethod
    @userview
    async def update_password(user_id: int, new_password: str):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                finally:
                    await session.rollback()
