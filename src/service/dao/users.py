import json
from sqlalchemy.exc import IntegrityError
from src.models.paramClasses import SchemaAddUser
from sqlalchemy import select, insert
from src.models.dbModels import Users
from src.db import async_session_maker
from src.service.dto.users import userview
from src.service.auth import get_hashed_password
from src.routers.responses import UserResponse


class User:

    @staticmethod
    @userview
    async def set(usrobj: SchemaAddUser):
        password = get_hashed_password(usrobj.password)
        stmt = insert(Users).values(username=usrobj.username,password=password, avatar=bytes(json.dumps(usrobj.avatar),'utf8'), email=usrobj.email)
        async with async_session_maker() as session:
            try:
                result = await session.execute(stmt)
                await session.commit()
            except IntegrityError:
                return UserResponse.ALREADY_EXISTS

    @staticmethod
    @userview
    async def get_user(user_id: int):
        stmt = select(Users).where(Users.user_id == user_id)
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            result = result.scalars().all()
            if result:
                return result[0]
            else:
                return UserResponse.NOT_FOUND

    @staticmethod
    @userview
    async def add_green_points(user_id: int, gp: int):
        return "suckass"

    @staticmethod
    @userview
    async def refactor_green_score(user_id: int, isGoodBoy: bool = False):
        return "suckass"

    @staticmethod
    @userview
    async def rename(user_id: int, new_name: str):
        return "suckass"

    @staticmethod
    @userview
    async def update_photo(user_id: int, new_photo):
        return "suckass"

    @staticmethod
    @userview
    async def update_password(user_id: int, new_password: str):
        return "suckass"
