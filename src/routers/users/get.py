from fastapi import APIRouter, Depends
from src.schemas.response import SchemaUser
from src.service.users import User
from src.authentication.auth import get_user_from_token

router = APIRouter(prefix="/users")


@router.get("/{user_id}",response_model=SchemaUser)
async def get_user(user_id: int = Depends(get_user_from_token)) -> SchemaUser | list[SchemaUser] | None:
    resp = await User.get_user(user_id)
    return resp


