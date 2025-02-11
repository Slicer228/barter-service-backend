from fastapi import APIRouter, Depends
from src.authentication.auth import get_user_from_token
from src.service.trades_api.get import FetchDataInteractor

router = APIRouter(prefix="/trades")


@router.get("/incoming")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await FetchDataInteractor.get(user_id, FetchDataInteractor.INCOMING)


@router.get("/outgoing")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await FetchDataInteractor.get(user_id, FetchDataInteractor.OUTGOING)


@router.get("/processed")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await FetchDataInteractor.get(user_id, FetchDataInteractor.PROCEED)


@router.get("/archived")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await FetchDataInteractor.get(user_id, FetchDataInteractor.ARCHIVE)

