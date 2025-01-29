from fastapi import APIRouter, Depends
from src.service.utils import get_user_from_token
from src.schemas.request import SchemaSendOffer
from src.service.dao.offers import Offers


router = APIRouter(prefix="/offers")


@router.post("/send")
async def send_offer(offer: SchemaSendOffer, user_id: int = Depends(get_user_from_token)):
    return await Offers.send_offer(offer.trade_id, offer.source_post_id, user_id)


@router.post("/accept")
async def send_offer(offer: SchemaSendOffer, user_id: int = Depends(get_user_from_token)):
    return await Offers.accept_offer(offer.trade_id, offer.source_post_id, user_id)


@router.post("/reject")
async def send_offer(offer: SchemaSendOffer, processed: bool, user_id: int = Depends(get_user_from_token)):
    return await Offers.reject_offer(offer.trade_id, offer.source_post_id, user_id, processed)


@router.post("/end")
async def send_offer(offer: SchemaSendOffer, user_id: int = Depends(get_user_from_token)):
    await Offers.end_offer(offer.trade_id, offer.source_post_id, user_id)

