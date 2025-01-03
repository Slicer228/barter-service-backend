from fastapi import APIRouter, Depends
from src.service.dao.posts import Posts
from src.schemas.request_s import SchemaAddPost
from src.utils import get_user_from_token

postPostsRouter = APIRouter(prefix="/posts")


@postPostsRouter.post("/add/")
async def create_post(post: SchemaAddPost,user_id: int = Depends(get_user_from_token)) -> int:
    resp = await Posts.add(post,user_id)
    return resp

