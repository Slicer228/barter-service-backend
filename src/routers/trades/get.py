from fastapi import APIRouter, Depends
from src.authentication.auth import get_user_from_token
from src.service.trades_api.get import FetchDataTradeInteractor

router = APIRouter(prefix="/trades")


@router.get("/incoming")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await FetchDataTradeInteractor.get(user_id, FetchDataTradeInteractor.INCOMING)


@router.get("/outgoing")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await FetchDataTradeInteractor.get(user_id, FetchDataTradeInteractor.OUTGOING)


@router.get("/processed")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await FetchDataTradeInteractor.get(user_id, FetchDataTradeInteractor.PROCEED)


@router.get("/archived")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await FetchDataTradeInteractor.get(user_id, FetchDataTradeInteractor.ARCHIVE)

