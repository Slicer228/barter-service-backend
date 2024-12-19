from src.utils import addLogAsync
from fastapi import APIRouter, HTTPException
from src.service.dao.users import User
from src.models.responseClasses import SchemaUser
from src.models.paramClasses import SchemaAddUser
from fastapi import Depends
from typing import Optional

postUsersRouter = APIRouter(prefix="/users")

@postUsersRouter.post("/register/")
async def create_user(user: SchemaAddUser = Depends()):
    resp = await User.set(user)
    return resp
