from fastapi import APIRouter, Depends
from src.schemas.response import UserSchema
from src.service.users_api.get import FetchDataUserInteractor
from src.authentication.auth import get_user_from_token

router = APIRouter(prefix="/users")


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int = Depends(get_user_from_token)) -> UserSchema | list[UserSchema] | None:
    resp = await FetchDataUserInteractor.get_user(user_id)
    return resp


