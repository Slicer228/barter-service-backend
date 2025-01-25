from src.service.dto.offers import offer_view
from src.service.db import async_session_maker
from src.models.db import UserTrades, UserPosts
from src.service.dao.posts import Posts
from sqlalchemy import select, insert, update
from src.schemas.response import SchemaOffer
from src.service.exceptions import (
    OfferNotFound,
    CannotInteractWithSelf,
    NotYours,
    TradeNotFound,
    OfferAlreadyExists,
    NotVerificated
)
from src.service.dao.enums import TradeTypes, PostStatus, TradeStatus
from src.service.dao.utils import (
    is_post_exists,
    is_trade_exists,
    is_user_exists,
    user_is_post_owner,
    check_post_params,
    check_trade_params,
    user_verificated
)
from typing import List
from src.service.dao.users import User


class Offers:

    @staticmethod
    async def _find_trade_post_by_post_id(session, post_id: int):
        stmt = select(UserTrades).where(
            UserTrades.post_id == post_id,
            UserTrades.utType == TradeTypes.POST.value
        )

        data = await session.execute(stmt)

        return data.scalars().first()

    @staticmethod
    async def _find_trades_by_id(session, trade_id: int, trade_type: TradeTypes, trade_status: TradeStatus):
        stmt = select(UserTrades).where(
            UserTrades.trade_id == trade_id,
            UserTrades.utType == trade_type.value,
            UserTrades.status == trade_status.value
        )

        data = await session.execute(stmt)
        data = data.scalars().all()
        return data if len(data) > 1 else data[0]

    @staticmethod
    async def _find_trades(
            session,
            user_id: int,
            trade_type: TradeTypes,
            trade_status: TradeStatus = None
    ):

        stmt = select(UserTrades)\
            .where(
            UserTrades.user_id == user_id,
            UserTrades.utType == trade_type.value,
            ((UserTrades.status == trade_status.value) if trade_status else 1==1)
            )

        data = await session.execute(stmt)

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
            if not await user_is_post_owner(session, trade.user_id, trade.trade_id):
                offers.append(
                    SchemaOffer(
                        post=await cls._find_post_by_trade(session, trade.trade_id),
                        source_post=(
                            await Posts.get(trade.post_id) if trade.post_id else await User.get_user(trade.user_id)
                        ),
                    )
                )

        return offers

    @staticmethod
    async def _find_offers_to_post(session, trade_id: int, trade_status: TradeStatus = TradeStatus.ACTIVE):
        stmt = select(UserTrades).where(
            UserTrades.trade_id == trade_id,
            UserTrades.utType == TradeTypes.OFFER.value,
            UserTrades.status == trade_status.value
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
            trades = await cls._find_trades(session, user_id, TradeTypes.OFFER, TradeStatus.IN_PROCESS)

            posts_in_process = await cls._find_trades(session, user_id, TradeTypes.POST, TradeStatus.IN_PROCESS)
            for post in posts_in_process:
                trades.extend(await cls._find_offers_to_post(session, post.trade_id, TradeStatus.IN_PROCESS))

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
            trades = await cls._find_trades(session, user_id, TradeTypes.OFFER, TradeStatus.ARCHIVED)

            posts_arhived = await cls._find_trades(session, user_id, TradeTypes.POST, TradeStatus.ARCHIVED)
            for post in posts_arhived:
                trades.extend(await cls._find_offers_to_post(session, post.trade_id, TradeStatus.ARCHIVED))

            archived_offers = []
            archived_offers.extend(await cls._generate_offers(session, trades))
            if archived_offers:
                return archived_offers
            else:
                raise OfferNotFound

    @staticmethod
    async def _set_status_to_other_offers(
            session,
            accepted_post_id: int,
            trade_id: int,
            status: TradeStatus
    ):
        try:
            stmt = update(UserTrades).where(
                UserTrades.trade_id == trade_id,
                UserTrades.utType == TradeTypes.OFFER.value,
                UserTrades.post_id != accepted_post_id,
                UserTrades.status != TradeStatus.REJECTED.value
            ).values(status=status.value)

            await session.execute(stmt)

        except BaseException as e:
            await session.rollback()
            raise e

    @staticmethod
    async def _set_trade_status(session, posts, trades, status: TradeStatus):
        try:
            for post in posts:
                stmt = update(UserPosts).where(*post).values(status=status.value)
                await session.execute(stmt)

            for trade in trades:
                stmt = update(UserTrades).where(*trade).values(status=status.value)
                await session.execute(stmt)
        except BaseException as e:
            await session.rollback()
            raise e

    @classmethod
    async def _set_status_to_trade_elements(
            cls,
            session,
            main_trade: UserTrades,
            offered_post_id: int,
            status: TradeStatus
    ):
        await cls._set_trade_status(
            session,
            [
                [
                    UserPosts.post_id == offered_post_id
                ],
                [
                    UserPosts.post_id == main_trade.post_id
                ],
            ],
            [
                [
                    UserTrades.trade_id == main_trade.trade_id,
                    UserTrades.utType == TradeTypes.OFFER.value,
                    UserTrades.post_id == offered_post_id,
                    UserTrades.status != TradeStatus.REJECTED.value
                ],
                [
                    UserTrades.trade_id == main_trade.trade_id,
                    UserTrades.utType == TradeTypes.POST.value
                ],
            ],
            status=status
        )

    @classmethod
    @offer_view
    async def send_offer(cls, trade_id: int, source_post_id: int, user_id: int):

        async def verify_params(session):
            nonlocal trade_id, source_post_id, user_id

            await user_verificated(session, user_id=user_id)
            await is_trade_exists(session, trade_id)
            await is_post_exists(session, source_post_id)
            await is_user_exists(session, user_id)
            if await user_is_post_owner(session, user_id, trade_id):
                raise CannotInteractWithSelf

            try:
                await check_trade_params(
                    session,
                    UserTrades.trade_id == trade_id,
                    UserTrades.user_id == user_id,
                    UserTrades.utType == TradeTypes.OFFER.value,
                    UserTrades.status != TradeStatus.REJECTED.value
                )
                raise OfferAlreadyExists
            except TradeNotFound:
                ...

            await check_trade_params(
                session,
                UserTrades.trade_id == trade_id,
                UserTrades.utType == TradeTypes.POST.value,
                UserTrades.status == TradeStatus.ACTIVE.value
            )

            await check_post_params(
                session,
                UserPosts.post_id == source_post_id,
                UserPosts.status == PostStatus.ACTIVE.value
            )

            await check_post_params(
                session,
                UserPosts.trade_id == trade_id,
                UserPosts.status == PostStatus.ACTIVE.value
            )

        async with async_session_maker() as session:
            async with session.begin():
                try:
                    await verify_params(session)

                    stmt = insert(UserTrades).values(
                        user_id=user_id,
                        post_id=source_post_id,
                        trade_id=trade_id,
                        utType=TradeTypes.OFFER.value
                    )
                    await session.execute(stmt)
                    await session.commit()
                except BaseException as e:
                    await session.rollback()
                    raise e

    @classmethod
    @offer_view
    async def accept_offer(cls, trade_id: int, source_post_id: int, user_id: int):
        async def verify_params(session):

            nonlocal trade_id, source_post_id, user_id

            await user_verificated(session, user_id=user_id)
            if not await user_is_post_owner(session, user_id, trade_id):
                raise NotYours
            await is_trade_exists(session, trade_id)
            await is_post_exists(session, source_post_id)
            await check_trade_params(
                session,
                UserTrades.trade_id == trade_id,
                UserTrades.post_id == source_post_id,
                UserTrades.utType == TradeTypes.OFFER.value,
                UserTrades.status == TradeStatus.ACTIVE.value
            )
            await check_trade_params(
                session,
                UserTrades.trade_id == trade_id,
                UserTrades.utType == TradeTypes.POST.value,
                UserTrades.user_id == user_id,
                UserTrades.status == TradeStatus.ACTIVE.value
            )
            await check_post_params(
                session,
                UserPosts.post_id == source_post_id,
                UserPosts.status == PostStatus.ACTIVE.value
            )
            await check_post_params(
                session,
                UserPosts.trade_id == trade_id,
                UserPosts.status == PostStatus.ACTIVE.value
            )

        async with async_session_maker() as session:

            async with session.begin():
                await verify_params(session)

                await cls._set_status_to_other_offers(session, source_post_id, trade_id, TradeStatus.FROZEN)
                source_post_trade = await cls._find_trade_post_by_post_id(session, source_post_id)
                await cls._set_status_to_other_offers(session, source_post_trade.post_id, source_post_trade.trade_id, TradeStatus.FROZEN)
                await cls._set_status_to_trade_elements(
                    session,
                    await cls._find_trades_by_id(session, trade_id, TradeTypes.POST, TradeStatus.ACTIVE),
                    source_post_id,
                    TradeStatus.IN_PROCESS
                )
                await session.commit()

            trade = await cls._find_trades(session, user_id, TradeTypes.POST)
            offer = await cls._generate_offers(session, trade)
            return offer

    @classmethod
    @offer_view
    async def reject_offer(cls, trade_id: int, source_post_id: int, user_id: int, processed: bool):
        async def verify_params(session):
            nonlocal trade_id, source_post_id, user_id, processed

            await user_verificated(session, user_id=user_id)
            await is_trade_exists(session, trade_id)
            await is_post_exists(session, source_post_id)
            await is_user_exists(session, user_id)
            if not await user_is_post_owner(session, user_id, trade_id):
                raise CannotInteractWithSelf

            status = TradeStatus.IN_PROCESS.value if processed else TradeStatus.ACTIVE.value

            await check_trade_params(
                session,
                UserTrades.trade_id == trade_id,
                UserTrades.post_id == source_post_id,
                UserTrades.status == status,
                UserTrades.utType == TradeTypes.OFFER.value
            )

            await check_trade_params(
                session,
                UserTrades.trade_id == trade_id,
                UserTrades.utType == TradeTypes.POST.value,
                UserTrades.user_id == user_id,
                UserTrades.status == status
            )
            await check_post_params(
                session,
                UserPosts.post_id == source_post_id,
                UserPosts.status == status
            )
            await check_post_params(
                session,
                UserPosts.trade_id == trade_id,
                UserPosts.status == status
            )

        async def roll_back_processed_offer(session):
            nonlocal trade_id, source_post_id, user_id
            await cls._set_status_to_other_offers(session, source_post_id, trade_id, TradeStatus.ACTIVE)
            source_post_trade = await cls._find_trade_post_by_post_id(session, source_post_id)
            await cls._set_status_to_other_offers(session, source_post_trade.post_id, source_post_trade.trade_id, TradeStatus.ACTIVE)
            await cls._set_status_to_trade_elements(
                session,
                await cls._find_trades_by_id(session, trade_id, TradeTypes.POST, TradeStatus.IN_PROCESS),
                source_post_id,
                TradeStatus.ACTIVE
            )


        async with async_session_maker() as session:
            async with session.begin():
                try:
                    await verify_params(session)

                    if processed:
                        await roll_back_processed_offer(session)

                    stmt = update(UserTrades).where(
                        UserTrades.trade_id == trade_id,
                        UserTrades.utType == TradeTypes.OFFER.value,
                        UserTrades.post_id == source_post_id
                    ).values(status=TradeStatus.REJECTED.value)
                    await session.execute(stmt)
                    await session.commit()

                except BaseException as e:
                    await session.rollback()
                    raise e

    @classmethod
    @offer_view
    async def end_offer(cls, trade_id: int, source_post_id: int, user_id: int):
        async def verify_params(session):
            nonlocal trade_id, source_post_id, user_id

            await user_verificated(session, user_id=user_id)
            if not await user_is_post_owner(session, user_id, trade_id):
                raise NotYours
            await is_trade_exists(session, trade_id)
            await is_post_exists(session, source_post_id)
            await check_trade_params(
                session,
                UserTrades.trade_id == trade_id,
                UserTrades.post_id == source_post_id,
                UserTrades.utType == TradeTypes.OFFER.value,
                UserTrades.status == TradeStatus.IN_PROCESS.value
            )
            await check_trade_params(
                session,
                UserTrades.trade_id == trade_id,
                UserTrades.utType == TradeTypes.POST.value,
                UserTrades.user_id == user_id,
                UserTrades.status == TradeStatus.IN_PROCESS.value
            )
            await check_post_params(
                session,
                UserPosts.post_id == source_post_id,
                UserPosts.status == PostStatus.PROCESS.value
            )
            await check_post_params(
                session,
                UserPosts.trade_id == trade_id,
                UserPosts.status == PostStatus.PROCESS.value
            )

        async with async_session_maker() as session:
            async with session.begin():
                await verify_params(session)

                await cls._set_status_to_other_offers(session, source_post_id, trade_id, TradeStatus.REJECTED)
                source_post_trade = await cls._find_trade_post_by_post_id(session, source_post_id)
                await cls._set_status_to_other_offers(session, source_post_trade.post_id, source_post_trade.trade_id, TradeStatus.REJECTED)
                await cls._set_status_to_trade_elements(
                    session,
                    await cls._find_trades_by_id(session, trade_id, TradeTypes.POST, TradeStatus.IN_PROCESS),
                    source_post_id,
                    TradeStatus.ARCHIVED
                )
                await session.commit()

            return await cls.get_archive(user_id)

