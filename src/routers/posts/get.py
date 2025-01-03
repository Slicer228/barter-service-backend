from fastapi import APIRouter
from src.schemas.response_s import SchemaPost
from src.service.dao.posts import Posts
from fastapi_cache.decorator import cache


getPostsRouter = APIRouter(prefix="/posts")


@getPostsRouter.get("/{post_id}")
@cache(expire=300)
async def get_posts(post_id: int) -> list[SchemaPost] | SchemaPost:
    resp = await Posts.get(post_id)
    return resp
