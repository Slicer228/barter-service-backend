from fastapi import APIRouter, Depends
from src.authentication.auth import get_user_from_token
from src.schemas.request import RequestTradeDataSchema
from src.service.trades_api.process import ProcessDataTradeInteractor


router = APIRouter(prefix="/trades")


@router.post("/send")
async def send_offer(offer: RequestTradeDataSchema, user_id: int = Depends(get_user_from_token)):
    return await ProcessDataTradeInteractor.update_trade(offer, user_id, ProcessDataTradeInteractor.SEND)


@router.post("/accept")
async def send_offer(offer: RequestTradeDataSchema, user_id: int = Depends(get_user_from_token)):
    return await ProcessDataTradeInteractor.update_trade(offer, user_id, ProcessDataTradeInteractor.ACCEPT)


@router.post("/reject")
async def send_offer(offer: RequestTradeDataSchema, processed: bool, user_id: int = Depends(get_user_from_token)):
    return await ProcessDataTradeInteractor.update_trade(offer, user_id, ProcessDataTradeInteractor.REJECT)


@router.post("/end")
async def send_offer(offer: RequestTradeDataSchema, user_id: int = Depends(get_user_from_token)):
    return await ProcessDataTradeInteractor.update_trade(offer, user_id, ProcessDataTradeInteractor.END)
