from src.service.dto.offers import offer_view
from src.db import async_session_maker
from src.models.dbModels import UserTrades, UserPosts
from src.service.dao.posts import Posts
from sqlalchemy import select, insert, update
from src.schemas.response_s import SchemaOffer
from src.exceptions import OfferNotFound, CannotInteractWithSelf
from src.service.dao.enums import TradeTypes, PostStatus, TradeStatus
from src.service.dao.utils import is_post_exists, is_trade_exists, is_user_exists, user_is_post_owner
from src.schemas.request_s import SchemaSendOffer
from typing import List


class Offers:

    @staticmethod
    async def _find_trades(
            session,
            user_id: int,
            trade_type: TradeTypes,
            trade_status: TradeStatus = None
    ):
        query = select(UserTrades)\
            .where(
            UserTrades.user_id == user_id,
            UserTrades.utType == trade_type.value,
            ((UserTrades.status == trade_status.value) if trade_status else 1==1)
            )
        #ТУТ ВОЗВРАЩАЕТ НА ВТОРОМ ЮЗЕРЕ ВСЕ ТРЕЙД АЙДИ 3
        data = await session.execute(query)

        return data.scalars().all()

    @staticmethod
    async def _find_post_by_trade(session, trade_id: int, status: PostStatus = None):
        stmt = select(UserPosts.post_id)\
                .where(
            UserPosts.trade_id == trade_id,
            (UserPosts.status == status.value) if status else 1==1
                    )
        data = await session.execute(stmt)
        data = data.scalars().first()

        return await Posts.get(data)

    @classmethod
    async def _generate_offers(cls, session, trades: List[UserTrades]):
        offers = []
        for trade in trades:
            offers.append(
                SchemaOffer(
                    post=await cls._find_post_by_trade(session, trade.trade_id),
                    source_post=await Posts.get(trade.post_id)
                )
            )

        return offers

    @staticmethod
    async def _find_offers_to_post(session, trade_id: int):
        stmt = select(UserTrades).where(
            UserTrades.trade_id == trade_id,
            UserTrades.utType == TradeTypes.OFFER.value
        )
        data = await session.execute(stmt)

        return data.scalars().all()

    @classmethod
    @offer_view
    async def get_incoming(cls, user_id: int):
        async with async_session_maker() as session:
            post_trades = await cls._find_trades(session, user_id, TradeTypes.POST)
            incoming_offers = []
            for post_trade in post_trades:
                incoming_offers.extend(
                    await cls._generate_offers(
                        session,
                        await cls._find_offers_to_post(session, post_trade.trade_id)
                    )
                )
            if incoming_offers:
                return incoming_offers
            else:
                raise OfferNotFound

    @classmethod
    @offer_view
    async def get_processing(cls, user_id: int):
        async with async_session_maker() as session:
            trades = await cls._find_trades(session, user_id, TradeTypes.POST, TradeStatus.IN_PROCESS)
            processing_offers = []
            processing_offers.extend(await cls._generate_offers(session, trades))
            if processing_offers:
                return processing_offers
            else:
                raise OfferNotFound

    @classmethod
    @offer_view
    async def get_outgoing(cls, user_id: int):
        async with async_session_maker() as session:
            outgoing_trades = await cls._find_trades(session, user_id, TradeTypes.OFFER)
            outgoing_offers = []
            outgoing_offers.extend(await cls._generate_offers(session, outgoing_trades))
            if outgoing_offers:
                return outgoing_offers
            else:
                raise OfferNotFound

    @classmethod
    @offer_view
    async def get_archive(cls, user_id: int):
        async with async_session_maker() as session:
            outgoing_trades = await cls._find_trades(session, user_id, TradeTypes.OFFER, TradeStatus.ARCHIVED)
            outgoing_offers = []
            outgoing_offers.extend(await cls._generate_offers(session, outgoing_trades))
            if outgoing_offers:
                return outgoing_offers
            else:
                raise OfferNotFound

    @staticmethod
    async def _freeze_offer(session, trade_id: int, unfreeze: bool = False):
        async with session.begin():
            try:
                stmt = update(UserTrades).where(
                    UserTrades.trade_id == trade_id,
                ).values(status=(TradeStatus.ACTIVE if unfreeze else TradeStatus.FROZEN))

                await session.execute(stmt)
            finally:
                await session.rollback()

    @classmethod
    async def _freeze_other_offers(cls, session, accepted_post_id: int, unfreeze: bool = False):
        all_offers = await cls._find_trades(session, accepted_post_id, TradeTypes.OFFER)
        all_offers = filter(
            lambda trade: trade.post_id != accepted_post_id,
            all_offers
        )
        for trade in all_offers:
            await cls._freeze_offer(session, trade.trade_id, unfreeze)

    @classmethod
    async def _trade_to_process(cls, session, trade_id: int, unprocess: bool = False):
        target_post = await cls._find_post_by_trade(session, trade_id)
        async with session.begin():
            try:
                trade_stmt = update(UserTrades).where(
                    UserTrades.trade_id == trade_id,
                    UserTrades.utType == TradeTypes.POST,
                ).values(status=(TradeStatus.ACTIVE if unprocess else TradeStatus.IN_PROCESS))
                post_stmt = update(UserPosts).where(
                    UserPosts.post_id == target_post.post_id
                ).values(post_id=(PostStatus.ACTIVE if unprocess else PostStatus.PROCESS))
                await session.execute(trade_stmt)
                await session.execute(post_stmt)
            finally:
                await session.rollback()

    @classmethod
    @offer_view
    async def send_offer(cls, trade_id: int, source_post_id: int, user_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    await is_trade_exists(session, trade_id)
                    await is_post_exists(session, source_post_id, PostStatus.ACTIVE)
                    await is_user_exists(session, user_id)
                    if await user_is_post_owner(session, user_id, trade_id):
                        raise CannotInteractWithSelf

                    stmt = insert(UserTrades).values(
                        user_id=user_id,
                        post_id=source_post_id,
                        trade_id=trade_id,
                        utType=TradeTypes.OFFER.value
                    )
                    await session.execute(stmt)
                    await session.commit()
                finally:
                    session.rollback()

    @classmethod
    @offer_view
    async def accept_offer(cls, trade_id: int, source_post_id: int, user_id: int):
        async with async_session_maker() as session:

            await user_is_post_owner(session, user_id, trade_id)
            await is_trade_exists(session, trade_id)
            await is_post_exists(session, source_post_id)

            await cls._freeze_other_offers(session, source_post_id)
            await cls._trade_to_process(session, trade_id)
            return await cls._generate_offers(session, await cls._find_trades(session, user_id, TradeTypes.POST))

    @classmethod
    @offer_view
    async def reject_offer(cls, trade_id: int, source_post_id: int):
        ...

    @classmethod
    @offer_view
    async def end_offer(cls, trade_id: int, source_post_id: int):
        ...

