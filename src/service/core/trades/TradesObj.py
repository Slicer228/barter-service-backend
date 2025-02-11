from sqlalchemy import update, insert
from src.models.db import UserTrades
from src.schemas.request import RequestTradeDataSchema
from src.service.core.trades import dao
from src.service.core.trades.validator import Validator
from src.service.dto.trades import trades_view
from src.exc.exceptions import OfferNotFound
from src.service.db import async_session_maker
from src.service.core.enums import TradeTypes, TradeStatus, OfferScenarios


@trades_view
async def get_incoming(user_id: int):
    async with async_session_maker() as session:
        post_trades = await dao.find_trades(session, user_id, TradeTypes.POST)
        incoming_offers = []
        for post_trade in post_trades:
            incoming_offers.extend(
                await dao.generate_offers(
                    session,
                    await dao.find_offers_to_post(session, post_trade.trade_id)
                )
            )
        if incoming_offers:
            return incoming_offers
        else:
            raise OfferNotFound


@trades_view
async def get_processing(user_id: int):
    async with async_session_maker() as session:
        trades = await dao.find_trades(session, user_id, TradeTypes.OFFER, TradeStatus.IN_PROCESS)

        posts_in_process = await dao.find_trades(session, user_id, TradeTypes.POST, TradeStatus.IN_PROCESS)
        for post in posts_in_process:
            trades.extend(await dao.find_offers_to_post(session, post.trade_id, TradeStatus.IN_PROCESS))

        processing_offers = []
        processing_offers.extend(await dao.generate_offers(session, trades))
        if processing_offers:
            return processing_offers
        else:
            raise OfferNotFound


@trades_view
async def get_outgoing(user_id: int):
    async with async_session_maker() as session:
        outgoing_trades = await dao.find_trades(session, user_id, TradeTypes.OFFER)
        outgoing_offers = []
        outgoing_offers.extend(await dao.generate_offers(session, outgoing_trades))
        if outgoing_offers:
            return outgoing_offers
        else:
            raise OfferNotFound


@trades_view
async def get_archive(user_id: int):
    async with async_session_maker() as session:
        trades = await dao.find_trades(session, user_id, TradeTypes.OFFER, TradeStatus.ARCHIVED)

        posts_arhived = await dao.find_trades(session, user_id, TradeTypes.POST, TradeStatus.ARCHIVED)
        for post in posts_arhived:
            trades.extend(await dao.find_offers_to_post(session, post.trade_id, TradeStatus.ARCHIVED))

        archived_offers = []
        archived_offers.extend(await dao.generate_offers(session, trades))
        if archived_offers:
            return archived_offers
        else:
            raise OfferNotFound


@trades_view
async def send_offer(offer_data: RequestTradeDataSchema, user_id: int, **kwargs):

    async with async_session_maker() as session:
        async with session.begin():
            try:
                await Validator.validate_offer_scenario(session, offer_data, user_id, OfferScenarios.SEND)

                stmt = insert(UserTrades).values(
                    user_id=user_id,
                    post_id=offer_data.source_post_id,
                    trade_id=offer_data.trade_id,
                    utType=TradeTypes.OFFER.value
                )
                await session.execute(stmt)
                await session.commit()
            except BaseException as e:
                await session.rollback()
                raise e


@trades_view
async def accept_offer(offer_data: RequestTradeDataSchema, user_id: int, **kwargs):

    async with async_session_maker() as session:

        async with session.begin():
            await Validator.validate_offer_scenario(session, offer_data, user_id, OfferScenarios.ACCEPT)

            await dao.set_status_to_other_offers(session, offer_data.source_post_id, offer_data.trade_id, TradeStatus.FROZEN)
            source_post_trade = await dao.find_trade_post_by_post_id(session, offer_data.source_post_id)
            await dao.set_status_to_other_offers(session, source_post_trade.post_id, source_post_trade.trade_id, TradeStatus.FROZEN)
            await dao.set_status_to_trade_elements(
                session,
                await dao.find_trades_by_id(session, offer_data.trade_id, TradeTypes.POST, TradeStatus.ACTIVE),
                offer_data.source_post_id,
                TradeStatus.IN_PROCESS
            )
            await session.commit()


@trades_view
async def reject_offer(offer_data: RequestTradeDataSchema, user_id: int, **kwargs):

    async def roll_back_processed_offer(session):

        await dao.set_status_to_other_offers(session, offer_data.source_post_id, offer_data.trade_id, TradeStatus.ACTIVE)
        source_post_trade = await dao.find_trade_post_by_post_id(session, offer_data.source_post_id)
        await dao.set_status_to_other_offers(session, source_post_trade.post_id, source_post_trade.trade_id, TradeStatus.ACTIVE)
        await dao.set_status_to_trade_elements(
            session,
            await dao.find_trades_by_id(session, offer_data.trade_id, TradeTypes.POST, TradeStatus.IN_PROCESS),
            offer_data.source_post_id,
            TradeStatus.ACTIVE
        )

    async with async_session_maker() as session:
        async with session.begin():
            try:
                await Validator.validate_offer_scenario(session, offer_data, user_id, OfferScenarios.REJECT)

                if kwargs['processed']:
                    await roll_back_processed_offer(session)

                stmt = update(UserTrades).where(
                    UserTrades.trade_id == offer_data.trade_id,
                    UserTrades.utType == TradeTypes.OFFER.value,
                    UserTrades.post_id == offer_data.source_post_id
                ).values(status=TradeStatus.REJECTED.value)
                await session.execute(stmt)
                await session.commit()

            except BaseException as e:
                await session.rollback()
                raise e


@trades_view
async def end_offer(offer_data: RequestTradeDataSchema, user_id: int, **kwargs):

    async with async_session_maker() as session:
        async with session.begin():
            await Validator.validate_offer_scenario(session, offer_data, user_id, OfferScenarios.END)

            await dao.set_status_to_other_offers(session, offer_data.source_post_id, offer_data.trade_id, TradeStatus.REJECTED)
            source_post_trade = await dao.find_trade_post_by_post_id(session, offer_data.source_post_id)
            await dao.set_status_to_other_offers(session, source_post_trade.post_id, source_post_trade.trade_id, TradeStatus.REJECTED)
            await dao.set_status_to_trade_elements(
                session,
                await dao.find_trades_by_id(session, offer_data.trade_id, TradeTypes.POST, TradeStatus.IN_PROCESS),
                offer_data.source_post_id,
                TradeStatus.ARCHIVED
            )
            await session.commit()

        return await dao.get_archive(user_id)