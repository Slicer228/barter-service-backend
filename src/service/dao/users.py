from src.models.paramClasses import SchemaAddUser
from sqlalchemy import select, insert
from src.models.dbModels import Users
from src.db import async_session_maker
from src.service.dto.users import userview


class User:

    @staticmethod
    @userview
    async def set(usrobj: SchemaAddUser):
        stmt = insert(Users).values(username=usrobj.username,password=usrobj.password, avatar=usrobj.avatar)
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            await session.commit()

    @staticmethod
    @userview
    async def get_user(user_id: int):
        stmt = select(Users).where(Users.user_id == user_id)
        async with async_session_maker() as session:
            result = await session.execute(stmt)
            return result.scalars().all()[0]

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
