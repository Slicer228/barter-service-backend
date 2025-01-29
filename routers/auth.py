from fastapi import Depends, APIRouter, Response, Request
from src.schemas.request import SchemaAddUser, SchemaAuthUser
from authentication.auth import create_access_token, get_user_from_token
from src.service.dao.users import User
from authentication.token_link import generate_refresh_token
from fastapi.responses import RedirectResponse, JSONResponse
from src.service.dao.auth import set_refresh_token, check_refresh_token


router = APIRouter(prefix="/auth")


@router.get("/logout/")
async def logout(response: Response, user_id=Depends(get_user_from_token)) -> None:
    if not isinstance(user_id, int):
        return user_id
    response.delete_cookie('access_token')


@router.post("/authorization/")
async def authorize_user(response: Response, user: SchemaAuthUser):
    user_id = (await User.get_user_from_email(user.email)).user_id
    token = create_access_token({'sub': str(user_id)})
    refresh_token = generate_refresh_token(token)
    await set_refresh_token(user_id, refresh_token['token'])
    response.set_cookie('access_token', token, httponly=True)
    return JSONResponse(refresh_token, status_code=200)


@router.post("/refresh")
async def login_user(response: Response, user: SchemaAuthUser):
    user_id = await User.auth(user)
    token = create_access_token({'sub': str(user_id)})
    response.set_cookie('access_token', token, httponly=True)
    return None


@router.post("/registration/")
async def create_user(response: Response, user: SchemaAddUser):
    await User.set(user)
    return await authorize_user(response, SchemaAuthUser(email=user.email, password=user.password))
