from src.exc.exceptions import ParentException
from src.service.core.trades import Trades


class FetchDataInteractor:
    OUTGOING = 1
    INCOMING = 2
    ARCHIVE = 3
    PROCEED = 4

    @classmethod
    async def get(cls, user_id: int, trade_prop: int):
        match trade_prop:
            case cls.ARCHIVE:
                return await Trades.get_archive(user_id)
            case cls.OUTGOING:
                return await Trades.get_outgoing(user_id)
            case cls.PROCEED:
                return await Trades.get_processing(user_id)
            case cls.INCOMING:
                return await Trades.get_incoming(user_id)
            case _: raise ParentException('No trade prop found')


