from fastapi import APIRouter, Depends, Response
from src.schemas.response_s import SchemaUser
from src.service.dao.users import User
from src.utils import get_user_from_token
from src.tasks.tasks import send_offer_notification
getUsersRouter = APIRouter(prefix="/users")


@getUsersRouter.get("/{user_id}",response_model=SchemaUser)
async def get_user(user_id: int = Depends(get_user_from_token)) -> SchemaUser | list[SchemaUser] | None:
    resp = await User.get_user(user_id)
    return resp

@getUsersRouter.get("/logout/",dependencies=[])
async def logout(response: Response) -> None:
    response.delete_cookie('access_token')
