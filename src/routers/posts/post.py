from fastapi import APIRouter, Depends
from src.service.posts_api import Posts
from src.schemas.request import AddPostSchema
from src.authentication.auth import get_user_from_token

router = APIRouter(prefix="/posts")


@router.post("/add/")
async def create_post(post: AddPostSchema, user_id: int = Depends(get_user_from_token)) -> int:
    resp = await Posts.add(post,user_id)
    return resp

