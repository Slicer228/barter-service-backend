from src.models.db import UserTrades, UserPosts
from src.service.core.enums import TradeTypes
from sqlalchemy import select
from src.exc.exceptions import ParentException, TradeNotFound


class ValidatorDAO:
    _stmt_prepared = select(
        UserTrades,
        UserPosts.post_id,
        UserPosts.post_status).join(UserPosts,
                                    UserPosts.trade_id == UserTrades.trade_id
                                    )

    @staticmethod
    async def _get_one_trade_from_data(data):
        if len(data) > 1:
            raise ParentException("Error in database")
        if len(data) == 0:
            raise TradeNotFound()
        return data[0]

    @classmethod
    async def get_owners_trade_by_trade_id(cls, session, trade_id: int):
        stmt = cls._stmt_prepared.where(
            UserTrades.trade_id == trade_id,
            UserTrades.utType == TradeTypes.POST.value
        )
        data = (await session.execute(stmt)).all()

        return await cls._get_one_trade_from_data(data)

    @classmethod
    async def get_owners_trade_by_post_id(cls, session, post_id: int):
        stmt = cls._stmt_prepared.where(
            UserTrades.post_id == post_id,
            UserTrades.utType == TradeTypes.POST.value
        )
        data = (await session.execute(stmt)).all()

        return await cls._get_one_trade_from_data(data)

    @classmethod
    async def get_offering_trade(cls, session, trade_id: int, source_post_id: int):
        stmt = cls._stmt_prepared.where(
            UserTrades.trade_id == trade_id,
            UserTrades.post_id == source_post_id,
            UserTrades.utType == TradeTypes.OFFER.value
        )

        data = (await session.execute(stmt)).all()

        return await cls._get_one_trade_from_data(data)