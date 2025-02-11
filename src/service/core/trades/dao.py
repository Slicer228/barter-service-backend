from src.models.db import UserTrades, UserPosts
from src.service.core.enums import TradeTypes, TradeStatus, PostStatus
from sqlalchemy import select, update
from typing import List
from src.service.core.utils_dao import user_is_post_owner
from src.schemas.response import TradeSchema
from src.service.posts_api.get import FetchDataPostInteractor
from src.service.users_api.get import FetchDataUserInteractor


async def find_trades(
        session,
        user_id: int,
        trade_type: TradeTypes,
        trade_status: TradeStatus = None
):
    stmt = select(UserTrades) \
        .where(
        UserTrades.user_id == user_id,
        UserTrades.utType == trade_type.value,
        ((UserTrades.trade_status == trade_status.value) if trade_status else 1 == 1)
    )

    data = await session.execute(stmt)

    return data.scalars().all()


async def generate_offers(session, trades: List[UserTrades]):
    async def find_post_by_trade(trade_id: int, status: PostStatus = None):
        stmt = select(UserPosts.post_id) \
            .where(
            UserPosts.trade_id == trade_id,
            (UserPosts.post_status == status.value) if status else 1 == 1
        )
        data = await session.execute(stmt)
        data = data.scalars().first()

        return await FetchDataPostInteractor.get_by_id(data)

    offers = []
    for trade in trades:
        if not await user_is_post_owner(session, trade.user_id, trade.trade_id):
            offers.append(
                TradeSchema(
                    post=await find_post_by_trade(session, trade.trade_id),
                    source_post=(
                        await FetchDataPostInteractor.get_by_id(trade.post_id)\
                            if trade.post_id\
                            else await FetchDataUserInteractor.get_user(trade.user_id)
                    ),
                )
            )

    return offers


async def find_offers_to_post(session, trade_id: int, trade_status: TradeStatus = TradeStatus.ACTIVE):
    stmt = select(UserTrades).where(
        UserTrades.trade_id == trade_id,
        UserTrades.utType == TradeTypes.OFFER.value,
        UserTrades.trade_status == trade_status.value
    )
    data = await session.execute(stmt)

    return data.scalars().all()


async def find_trade_post_by_post_id(session, post_id: int):
    stmt = select(UserTrades).where(
        UserTrades.post_id == post_id,
        UserTrades.utType == TradeTypes.POST.value
    )

    data = await session.execute(stmt)

    return data.scalars().first()


async def find_trades_by_id(session, trade_id: int, trade_type: TradeTypes, trade_status: TradeStatus):
    stmt = select(UserTrades).where(
        UserTrades.trade_id == trade_id,
        UserTrades.utType == trade_type.value,
        UserTrades.trade_status == trade_status.value
    )

    data = await session.execute(stmt)
    data = data.scalars().all()
    return data if len(data) > 1 else data[0]


async def set_status_to_other_offers(
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
            UserTrades.trade_status != TradeStatus.REJECTED.value
        ).values(status=status.value)

        await session.execute(stmt)

    except BaseException as e:
        await session.rollback()
        raise e


async def set_trade_status(session, posts, trades, status: TradeStatus):
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


async def set_status_to_trade_elements(
        session,
        main_trade: UserTrades,
        offered_post_id: int,
        status: TradeStatus
):
    await set_trade_status(
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
                UserTrades.trade_status != TradeStatus.REJECTED.value
            ],
            [
                UserTrades.trade_id == main_trade.trade_id,
                UserTrades.utType == TradeTypes.POST.value
            ],
        ],
        status=status
    )
