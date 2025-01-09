from src.service.dto.offers import offerView
from src.db import async_session_maker
from src.models.dbModels import User_trades
from src.service.dao.posts import Posts
from sqlalchemy import select


class Offers:

    @staticmethod
    @offerView
    async def get_incoming(user_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(User_trades.post_id).join(User_trades.active).where(User_trades.user_id == user_id,User_trades.utType == 'post')
                data = await session.execute(query)
                print(data)


    @staticmethod
    @offerView
    async def get_processing(user_id: int):
        pass

    @staticmethod
    @offerView
    async def get_outgoing(user_id: int):
        pass

    @staticmethod
    @offerView
    async def get_archive(user_id: int):
        pass