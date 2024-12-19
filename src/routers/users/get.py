from src.utils import addLogAsync
from fastapi import APIRouter, HTTPException
from src.models.responseClasses import SchemaUser
from src.service.dao.users import User


getUsersRouter = APIRouter(prefix="/users")


@getUsersRouter.get("/user/{user_id}",response_model=SchemaUser)
async def get_user(user_id: int):
    resp = await User.get_user(user_id)
    return resp