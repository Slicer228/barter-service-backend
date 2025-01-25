from fastapi import APIRouter, Response
from src.service.dao.users import User
from src.schemas.request import SchemaAddUser, SchemaAuthUser
from src.service.auth import create_access_token
router = APIRouter(prefix="/users")


@router.post("/register/")
async def create_user(response: Response,user: SchemaAddUser):
    user_id = await User.set(user)
    token = create_access_token({'sub': str(user_id)})
    response.set_cookie('access_token', token, httponly=True)
    return None


@router.post("/auth/")
async def login_user(response: Response,user: SchemaAuthUser):
    user_id = await User.auth(user)
    token = create_access_token({'sub': str(user_id)})
    response.set_cookie('access_token', token, httponly=True)
    return None
