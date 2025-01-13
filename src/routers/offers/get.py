from fastapi import APIRouter, Depends
from src.utils import get_user_from_token
from src.service.dao.offers import Offers

getOffersRouter = APIRouter(prefix="/offers")


@getOffersRouter.get("/incoming")
async def get_incoming_offers(user_id: int = Depends(get_user_from_token)):
    return await Offers.get_incoming(user_id)

