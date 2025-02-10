from fastapi import APIRouter, Depends
from src.authentication.auth import get_user_from_token
from src.schemas.request import SchemaSendOffer
from src.service.trades import OfferSignals


router = APIRouter(prefix="/trades")


@router.post("/send")
async def send_offer(offer: SchemaSendOffer, user_id: int = Depends(get_user_from_token)):
    return await OfferSignals.send_offer(offer, user_id)


@router.post("/accept")
async def send_offer(offer: SchemaSendOffer, user_id: int = Depends(get_user_from_token)):
    return await OfferSignals.accept_offer(offer, user_id)


@router.post("/reject")
async def send_offer(offer: SchemaSendOffer, processed: bool, user_id: int = Depends(get_user_from_token)):
    return await OfferSignals.reject_offer(offer, user_id, processed)


@router.post("/end")
async def send_offer(offer: SchemaSendOffer, user_id: int = Depends(get_user_from_token)):
    await OfferSignals.end_offer(offer, user_id)

