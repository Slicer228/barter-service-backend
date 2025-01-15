from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.dbModels import User_posts, Trades, Users, User_trades
from src.exceptions import PostNotFound, ParentException, TradeNotFound, UserNotFound
from src.service.dao.enums import PostStatus, TradeTypes
from src.db import async_session_maker


class _InternalFuncs:

    @staticmethod
    async def prepare_post_stmt(post_id: int = None, trade_id: int = None, post_status: PostStatus = PostStatus.ACTIVE):
        if not post_id and not trade_id:
            raise ParentException('call error')
        if post_id and trade_id:
            raise ParentException('call error')

        if post_id:
            return select(User_posts.post_id).where(
            User_posts.post_id == post_id,
            User_posts.status == post_status.value
            )
        else:
            return select(User_posts.trade_id).where(
                User_posts.trade_id == trade_id,
                User_posts.status == post_status.value
            )

    @staticmethod
    async def check_if_post_exists(session, stmt):
        data = await session.execute(stmt)
        data = data.scalars().all()
        if data and len(data) == 1:
            return
        else:
            if len(data) > 1:
                raise ParentException('Too many post on one ID')
            else:
                raise PostNotFound("Post not found")


async def is_post_exists(session, post_id: int, post_status: PostStatus):
    stmt = await _InternalFuncs.prepare_post_stmt(post_id=post_id, post_status=post_status)
    await _InternalFuncs.check_if_post_exists(session, stmt)


async def is_trade_exists(session, trade_id: int, post_status: PostStatus = PostStatus.ACTIVE):
    stmt = select(Trades.trade_id).where(Trades.trade_id == trade_id)
    data = await session.execute(stmt)
    data = data.scalars().all()
    if data and len(data) == 1:
        stmt = await _InternalFuncs.prepare_post_stmt(trade_id=trade_id, post_status=post_status)
        await _InternalFuncs.check_if_post_exists(session, stmt)
        return
    else:
        if len(data) > 1:
            raise ParentException('Too many trades on one ID')
        else:
            raise TradeNotFound


async def is_user_exists(session, user_id: int):
    stmt = select(Users.user_id).where(Users.user_id == user_id)
    data = await session.execute(stmt)
    data = data.scalars().all()
    if data and len(data) == 1:
        return
    else:
        if len(data) > 1:
            raise ParentException('Too many users on one ID')
        else:
            raise UserNotFound


async def user_is_post_owner(session, user_id: int, trade_id: int):
    stmt = select(User_trades.user_id).where(
        User_trades.user_id == user_id,
        User_trades.trade_id == trade_id,
        User_trades.utType == TradeTypes.POST.value
    )
    data = await session.execute(stmt)
    data = data.scalars().all()

    if len(data) > 1:
        raise ParentException('Too many owners on one post')

    if data:
        return True
    else:
        return False


async def get_trade_owner_email(trade_id: int):
    async with async_session_maker() as session:
        stmt = select(User_trades.user_id).where(
            User_trades.trade_id == trade_id,
            User_trades.utType == TradeTypes.POST.value
        )
        data = await session.execute(stmt)
        data = data.scalars().first()

        stmt = select(Users.email).where(Users.user_id == data)
        data = await session.execute(stmt)
        data = data.scalars().first()

        return data


