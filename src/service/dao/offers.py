from src.service.dto.offers import offer_view
from src.db import async_session_maker
from src.models.dbModels import User_trades, User_posts
from src.service.dao.posts import Posts
from sqlalchemy import select
from src.schemas.response_s import SchemaOffer, SchemaPost
from src.exceptions import PostNotFound


class Offers:

    @staticmethod
    async def _find_trades(session, user_id: int):
        query = select(User_trades.trade_id)\
            .join(User_trades.active)\
            .where(
            User_trades.user_id == user_id,
            User_trades.utType == 'post'
            )
        data = await session.execute(query)
        return data.scalars().all()

    @staticmethod
    async def _find_post_by_trade(session, trade_id: int, status: str):
        stmt = select(User_posts.post_id)\
                .where(
                    User_posts.trade_id == trade_id,
                    User_posts.status == status
                    )
        data = await session.execute(stmt)
        data = data.scalars().first()
        return await Posts.get(data)

    @staticmethod
    async def _generate_offers(session, trade_id: int, post: SchemaPost):
        stmt = select(User_trades.post_id)\
            .where(User_trades.trade_id == trade_id,
                   User_trades.utType == 'offer'
                   )
        data = await session.execute(stmt)
        data = data.scalars().all()
        posts_and_users = [
            SchemaOffer(
                post = post,
                source_post = await Posts.get(item)
            )
            for item in data
        ]

        return posts_and_users

    @classmethod
    @offer_view
    async def get_incoming(cls, user_id: int):
        async with async_session_maker() as session:
            post_trades = await cls._find_trades(session, user_id)
            incoming_offers = []
            for trade_id in post_trades:
                post = await cls._find_post_by_trade(session, trade_id, 'active')
                if post:
                    incoming_offers.extend(await cls._generate_offers(session, trade_id, post))
                else:
                    raise PostNotFound('empty trade!')
            if incoming_offers:
                return incoming_offers
            else:
                raise PostNotFound('you have not any incoming posts!')

    @staticmethod
    @offer_view
    async def get_processing(user_id: int):
        async with async_session_maker() as session:
            ...

    @staticmethod
    @offer_view
    async def get_outgoing(user_id: int):
        pass

    @staticmethod
    @offer_view
    async def get_archive(user_id: int):
        pass

    @classmethod
    @offer_view
    async def send_offer(cls):
        ...

    @classmethod
    @offer_view
    async def accept_offer(cls, trade_id: int, source_post_id: int):
        ...

    @classmethod
    @offer_view
    async def reject_offer(cls, trade_id: int, source_post_id: int):
        ...

    @classmethod
    @offer_view
    async def end_offer(cls, trade_id: int, source_post_id: int):
        ...

