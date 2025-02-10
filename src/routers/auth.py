from fastapi import Depends, APIRouter, Response, Request
from src.schemas.request import SchemaAddUser, SchemaAuthUser
from src.authentication.auth import create_access_token, get_user_from_token, get_user_id_from_token, verify_password
from src.service.users import User
from src.authentication.token_link import generate_refresh_token, check_rt_expired, verify_refresh_token

router = APIRouter(prefix="/auth")


@router.get("/logout/")
async def logout(response: Response, user_id=Depends(get_user_from_token)) -> None:
    response.delete_cookie('access_token')


@router.post("/authorization/")
async def authorize_user(response: Response, user: SchemaAuthUser):
    user_obj = await User.get_user_from_email(user.email)
    await verify_password(user.password, user_obj.password)
    access_token = create_access_token({'sub': str(user_obj.user_id)})
    refresh_token = generate_refresh_token(access_token)
    await User.set_refresh_token(user_obj.user_id, refresh_token)
    response.set_cookie('access_token', access_token, httponly=True)
    return refresh_token['token']


@router.post("/refresh")
async def refresh_tokens(request: Request, response: Response, refresh_token: str):
    access_token = request.cookies.get('access_token')
    verify_refresh_token(access_token, refresh_token)
    user_id = (await User.get_user(await get_user_id_from_token(access_token))).user_id
    exp = await User.check_rt_and_get_exp(user_id, refresh_token)
    check_rt_expired(exp)
    new_access_token = create_access_token({'sub': str(user_id)})
    new_refresh_token = generate_refresh_token(new_access_token)
    await User.set_refresh_token(user_id, new_refresh_token)
    response.set_cookie('access_token', new_access_token, httponly=True)
    return new_refresh_token['token']


@router.post("/registration/")
async def create_user(response: Response, user: SchemaAddUser):
    await User.set(user)
    return await authorize_user(response, SchemaAuthUser(email=user.email, password=user.password))
