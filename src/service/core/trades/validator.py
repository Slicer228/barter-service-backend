from src.schemas.request import RequestTradeDataSchema
from sqlalchemy import select
from src.models.db import UserTrades, UserPosts
from src.service.core.enums import TradeTypes, PostTypes, PostStatus, TradeStatus, OfferScenarios
from src.exc.exceptions import ParentException, TradeNotFound, BadRequest, NotYours
from src.service.core.trades.validator_dao import ValidatorDAO


class Validator:

    @staticmethod
    async def _send_offer_scenario(session, offer_data: RequestTradeDataSchema, user_id: int):
        dest_trade = await ValidatorDAO.get_owners_trade_by_trade_id(session, offer_data.trade_id)

        if dest_trade.post_status != PostStatus.ACTIVE.value or dest_trade.trade_status != TradeStatus.ACTIVE.value:
            raise BadRequest("Inactive trade")

        if dest_trade.post_type == PostTypes.GIFT.value:
            if not offer_data.source_post_id == 0:
                raise BadRequest("Source post id is invalid")

        src_trade = await ValidatorDAO.get_offering_trade(session, offer_data.source_post_id, offer_data.trade_id)

        if src_trade.post_status != PostStatus.ACTIVE.value or src_trade.trade_status != TradeStatus.ACTIVE.value:
            raise BadRequest("Inactive trade")

        if src_trade.user_id != user_id:
            raise NotYours()

    @staticmethod
    async def _accept_offer_scenario(session, offer_data: RequestTradeDataSchema, user_id: int):
        dest_trade = await ValidatorDAO.get_owners_trade_by_trade_id(session, offer_data.trade_id)

        if dest_trade.post_type == PostTypes.GIFT.value:
            if not offer_data.source_post_id == 0:
                raise BadRequest("Source post id is invalid")

        if dest_trade.user_id != user_id:
            raise NotYours()

        if dest_trade.trade_status != TradeStatus.ACTIVE.value or dest_trade.post_status != PostStatus.ACTIVE.value:
            raise BadRequest("Inactive trade")

        src_trade = await ValidatorDAO.get_offering_trade(session, offer_data.source_post_id, offer_data.trade_id)

        if src_trade.trade_status != TradeStatus.ACTIVE.value or src_trade.post_status != PostStatus.ACTIVE.value:
            raise BadRequest("Inactive trade")

    @staticmethod
    async def _reject_offer_scenario(session, offer_data: RequestTradeDataSchema, user_id: int):
        dest_trade = await ValidatorDAO.get_owners_trade_by_trade_id(session, offer_data.trade_id)
        src_trade = await ValidatorDAO.get_offering_trade(session, offer_data.source_post_id, offer_data.trade_id)

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
        dest_trade = await ValidatorDAO.get_owners_trade_by_trade_id(session, offer_data.trade_id)

        if dest_trade.post_type == PostTypes.GIFT.value:
            if not offer_data.source_post_id == 0:
                raise BadRequest("Source post id is invalid")

        if dest_trade.user_id != user_id:
            raise NotYours()

        if dest_trade.trade_status != TradeStatus.IN_PROCESS.value or dest_trade.post_status != PostStatus.IN_PROCESS.value:
            raise BadRequest("Inactive trade")

        src_trade = await ValidatorDAO.get_offering_trade(session, offer_data.source_post_id, offer_data.trade_id)

        if src_trade.trade_status != TradeStatus.IN_PROCESS.value or src_trade.post_status != PostStatus.IN_PROCESS.value:
            raise BadRequest("Inactive trade")

    @classmethod
    async def validate_offer_scenario(cls, session, offer_data: RequestTradeDataSchema, user_id: int, scenario: OfferScenarios):
        match scenario.value:
            case OfferScenarios.SEND.value: await cls._send_offer_scenario(session, offer_data, user_id)
            case OfferScenarios.END.value: await cls._end_offer_scenario(session, offer_data, user_id)
            case OfferScenarios.ACCEPT.value: await cls._accept_offer_scenario(session, offer_data, user_id)
            case OfferScenarios.REJECT.value: await cls._reject_offer_scenario(session, offer_data, user_id)
