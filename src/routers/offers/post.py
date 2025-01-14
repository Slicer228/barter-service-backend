from fastapi import APIRouter, Depends
from src.utils import get_user_from_token
from src.schemas.request_s import SchemaSendOffer
from src.service.dao.offers import Offers


postOffersRouter = APIRouter(prefix="/offers")


@postOffersRouter.post("/send")
async def send_offer(offer: SchemaSendOffer, user_id: int = Depends(get_user_from_token)):
    await Offers.send_offer(user_id, offer)
