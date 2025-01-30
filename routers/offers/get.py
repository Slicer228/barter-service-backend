from fastapi import APIRouter, Depends
from authentication.auth import get_user_from_token
from src.service.dao.offers import Offers

router = APIRouter(prefix="/offers")


@router.get("/incoming")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await Offers.get_incoming(user_id)


@router.get("/outgoing")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await Offers.get_outgoing(user_id)


@router.get("/processed")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await Offers.get_processing(user_id)


@router.get("/archived")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await Offers.get_archive(user_id)

