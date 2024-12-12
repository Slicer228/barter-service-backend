from src.utils import addLogAsync
from fastapi import APIRouter
from src.models.responseClasses import SchemaUser
from src.service.dao.users import User

getUsersRouter = APIRouter(prefix="/users")


@getUsersRouter.get("/user/{user_id}",response_model=SchemaUser)
async def get_user(user_id: str):
    try:
        return await User.get_user(user_id)
    except Exception as e:
        await addLogAsync(e)
        return 0