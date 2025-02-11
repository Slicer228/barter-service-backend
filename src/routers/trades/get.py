from fastapi import APIRouter, Depends
from src.authentication.auth import get_user_from_token
from src.service.trades_api import GetOffers

router = APIRouter(prefix="/trades")


@router.get("/incoming")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await GetOffers.get_incoming(user_id)


@router.get("/outgoing")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await GetOffers.get_outgoing(user_id)


@router.get("/processed")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await GetOffers.get_processing(user_id)


@router.get("/archived")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await GetOffers.get_archive(user_id)

