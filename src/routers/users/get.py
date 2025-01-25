from fastapi import APIRouter, Depends, Response
from src.schemas.response import SchemaUser
from src.service.dao.users import User
from src.service.utils import get_user_from_token

router = APIRouter(prefix="/users")


@router.get("/{user_id}",response_model=SchemaUser)
async def get_user(user_id: int = Depends(get_user_from_token)) -> SchemaUser | list[SchemaUser] | None:
    resp = await User.get_user(user_id)
    return resp


@router.get("/logout/",dependencies=[])
async def logout(response: Response) -> None:
    response.delete_cookie('access_token')
