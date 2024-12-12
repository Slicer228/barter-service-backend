from src.utils import addLogAsync
from fastapi import APIRouter
from src.service.dao.users import User
from src.models.responseClasses import SchemaUser
from src.models.paramClasses import SchemaAddUser
from fastapi import Depends
from typing import Optional

postUsersRouter = APIRouter(prefix="/users")


@postUsersRouter.post("/add/",response_model=Optional[SchemaUser])
async def create_user(user: SchemaAddUser = Depends()):
    await User.set(user)