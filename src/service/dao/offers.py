from src.service.dto.offers import offer_view
from src.db import async_session_maker
from src.models.dbModels import User_trades, User_posts
from src.service.dao.posts import Posts
from sqlalchemy import select, insert
from src.schemas.response_s import SchemaOffer, SchemaPost
from src.exceptions import PostNotFound, CannotInteractWithSelf
from src.service.dao.enums import TradeTypes, PostStatus
from src.service.dao.utils import is_post_exists, is_trade_exists, is_user_exists, user_is_post_owner
from src.schemas.request_s import SchemaSendOffer


class Offers:

    @staticmethod
    async def _find_trades(session, user_id: int, trade_type: TradeTypes):
        query = select(User_trades.trade_id)\
            .join(User_trades.active)\
            .where(
            User_trades.user_id == user_id,
            User_trades.utType == trade_type.value
            )
        data = await session.execute(query)
        return data.scalars().all()

    @staticmethod
    async def _find_post_by_trade(session, trade_id: int, status: PostStatus):
        stmt = select(User_posts.post_id)\
                .where(
                    User_posts.trade_id == trade_id,
                    User_posts.status == status.value
                    )
        data = await session.execute(stmt)
        data = data.scalars().first()
        return await Posts.get(data)

    @staticmethod
    async def _generate_offers(session, trade_id: int, target: SchemaPost):
        stmt = select(User_trades.post_id)\
            .where(User_trades.trade_id == trade_id,
                   User_trades.utType == TradeTypes.OFFER.value
                   )
        data = await session.execute(stmt)
        data = data.scalars().all()
        posts_and_users = [
            SchemaOffer(
                post=target,
                source_post=await Posts.get(item)
            )
            for item in data
        ]

        return posts_and_users

    @classmethod
    @offer_view
    async def get_incoming(cls, user_id: int):
        async with async_session_maker() as session:
            post_trades = await cls._find_trades(session, user_id, TradeTypes.POST)
            incoming_offers = []
            for trade_id in post_trades:
                post = await cls._find_post_by_trade(session, trade_id, PostStatus.ACTIVE)
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
    async def send_offer(cls, source_user_id: int, offer: SchemaSendOffer):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    await is_trade_exists(session, offer.trade_id)
                    await is_post_exists(session, offer.source_post_id, PostStatus.ACTIVE)
                    await is_user_exists(session, source_user_id)
                    if await user_is_post_owner(session, source_user_id, offer.trade_id):
                        raise CannotInteractWithSelf

                    stmt = insert(User_trades).values(
                        user_id=source_user_id,
                        post_id=offer.source_post_id,
                        trade_id=offer.trade_id,
                        utType=TradeTypes.OFFER.value
                    )
                    await session.execute(stmt)
                    await session.commit()
                finally:
                    session.rollback()

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

