from fastapi import Depends, APIRouter, Response, Request
from src.schemas.request import SchemaAddUser, SchemaAuthUser
from authentication.auth import create_access_token, get_user_from_token, get_user_id_from_token
from src.service.dao.users import User
from authentication.token_link import generate_refresh_token, check_rt_expired, verify_refresh_token
from fastapi.responses import RedirectResponse, JSONResponse


router = APIRouter(prefix="/auth")


@router.get("/logout/")
async def logout(response: Response, user_id=Depends(get_user_from_token)) -> None:
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
async def refresh_tokens(request: Request, response: Response, refresh_token: dict = Depends(check_rt_expired)):
    access_token = request.cookies.get('access_token')
    verify_refresh_token(access_token, refresh_token['token'])
    user_id = (await User.get_user(await get_user_id_from_token(access_token))).user_id
    await User.verify_refresh_token(user_id, refresh_token['token'])
    await User.set_refresh_token(user_id, refresh_token['token'])
    new_access_token = create_access_token({'sub': str(user_id)})
    response.set_cookie('access_token', new_access_token, httponly=True)
    return JSONResponse(generate_refresh_token(new_access_token), status_code=200)


@router.post("/registration/")
async def create_user(response: Response, user: SchemaAddUser):
    await User.set(user)
    return await authorize_user(response, SchemaAuthUser(email=user.email, password=user.password))
