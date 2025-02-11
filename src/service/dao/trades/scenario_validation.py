from src.schemas.request import RequestTradeDataSchema
from sqlalchemy import select
from src.models.db import UserTrades, UserPosts
from src.service.dao.enums import TradeTypes, PostTypes, PostStatus, TradeStatus, OfferScenarios
from src.exc.exceptions import ParentException, TradeNotFound, BadRequest, NotYours


class DataFetcher:

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


class Validator:

    @staticmethod
    async def _send_offer_scenario(session, offer_data: RequestTradeDataSchema, user_id: int):
        dest_trade = await DataFetcher.get_owners_trade_by_trade_id(session, offer_data.trade_id)

        if dest_trade.post_status != PostStatus.ACTIVE.value or dest_trade.trade_status != TradeStatus.ACTIVE.value:
            raise BadRequest("Inactive trade")

        if dest_trade.post_type == PostTypes.GIFT.value:
            if not offer_data.source_post_id == 0:
                raise BadRequest("Source post id is invalid")

        src_trade = await DataFetcher.get_offering_trade(session, offer_data.source_post_id, offer_data.trade_id)

        if src_trade.post_status != PostStatus.ACTIVE.value or src_trade.trade_status != TradeStatus.ACTIVE.value:
            raise BadRequest("Inactive trade")

        if src_trade.user_id != user_id:
            raise NotYours()

    @staticmethod
    async def _accept_offer_scenario(session, offer_data: RequestTradeDataSchema, user_id: int):
        dest_trade = await DataFetcher.get_owners_trade_by_trade_id(session, offer_data.trade_id)

        if dest_trade.post_type == PostTypes.GIFT.value:
            if not offer_data.source_post_id == 0:
                raise BadRequest("Source post id is invalid")

        if dest_trade.user_id != user_id:
            raise NotYours()

        if dest_trade.trade_status != TradeStatus.ACTIVE.value or dest_trade.post_status != PostStatus.ACTIVE.value:
            raise BadRequest("Inactive trade")

        src_trade = await DataFetcher.get_offering_trade(session, offer_data.source_post_id, offer_data.trade_id)

        if src_trade.trade_status != TradeStatus.ACTIVE.value or src_trade.post_status != PostStatus.ACTIVE.value:
            raise BadRequest("Inactive trade")

    @staticmethod
    async def _reject_offer_scenario(session, offer_data: RequestTradeDataSchema, user_id: int):
        dest_trade = await DataFetcher.get_owners_trade_by_trade_id(session, offer_data.trade_id)
        src_trade = await DataFetcher.get_offering_trade(session, offer_data.source_post_id, offer_data.trade_id)

        if (dest_trade.trade_status == TradeStatus.ACTIVE.value and dest_trade.post_status == PostStatus.ACTIVE.value\
            and src_trade.post_status == PostStatus.ACTIVE.value and src_trade.trade_status == TradeStatus.ACTIVE.value)\
            or (dest_trade.trade_status == TradeStatus.IN_PROCESS.value and dest_trade.post_status == PostStatus.IN_PROCESS.value\
            and src_trade.post_status == PostStatus.IN_PROCESS.value and src_trade.trade_status == TradeStatus.IN_PROCESS.value):

            if dest_trade.user_id != user_id or src_trade.user_id != user_id:
                raise NotYours()

            if dest_trade.post_type == PostTypes.GIFT.value:
                if not offer_data.source_post_id == 0:
                    raise BadRequest("Source post id is invalid")

        else:
            raise BadRequest()

    @staticmethod
    async def _end_offer_scenario(session, offer_data: RequestTradeDataSchema, user_id: int):
        dest_trade = await DataFetcher.get_owners_trade_by_trade_id(session, offer_data.trade_id)

        if dest_trade.post_type == PostTypes.GIFT.value:
            if not offer_data.source_post_id == 0:
                raise BadRequest("Source post id is invalid")

        if dest_trade.user_id != user_id:
            raise NotYours()

        if dest_trade.trade_status != TradeStatus.IN_PROCESS.value or dest_trade.post_status != PostStatus.IN_PROCESS.value:
            raise BadRequest("Inactive trade")

        src_trade = await DataFetcher.get_offering_trade(session, offer_data.source_post_id, offer_data.trade_id)

        if src_trade.trade_status != TradeStatus.IN_PROCESS.value or src_trade.post_status != PostStatus.IN_PROCESS.value:
            raise BadRequest("Inactive trade")

    @classmethod
    async def validate_offer_scenario(cls, session, offer_data: RequestTradeDataSchema, user_id: int, scenario: OfferScenarios):
        match scenario.value:
            case OfferScenarios.SEND.value: await cls._send_offer_scenario(session, offer_data, user_id)
            case OfferScenarios.END.value: await cls._end_offer_scenario(session, offer_data, user_id)
            case OfferScenarios.ACCEPT.value: await cls._accept_offer_scenario(session, offer_data, user_id)
            case OfferScenarios.REJECT.value: await cls._reject_offer_scenario(session, offer_data, user_id)
