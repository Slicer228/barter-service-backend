from src.schemas.request import RequestTradeDataSchema
from src.exc.exceptions import ParentException
from src.service.core.trades import Trades


class ProcessDataInteractor:
    SEND = 5
    ACCEPT = 6
    REJECT = 7
    END = 8

    @classmethod
    async def update_trade(cls, trade_data: RequestTradeDataSchema, user_id: int, activity_prop: int, **kwargs):
        match activity_prop:
            case cls.SEND:
                return await Trades.send_offer(trade_data, user_id, kwargs)
            case cls.ACCEPT:
                return await Trades.accept_offer(trade_data, user_id, kwargs)
            case cls.REJECT:
                return await Trades.reject_offer(trade_data, user_id, kwargs)
            case cls.END:
                return await Trades.end_offer(trade_data, user_id, kwargs)
            case _:
                raise ParentException('No activity prop found')
