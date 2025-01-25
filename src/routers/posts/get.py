from fastapi import APIRouter
from src.schemas.response import SchemaPost
from src.service.dao.posts import Posts


getPostsRouter = APIRouter(prefix="/posts")


@getPostsRouter.get("/{post_id}")
async def get_posts(post_id: int) -> list[SchemaPost] | SchemaPost:
    resp = await Posts.get(post_id)
    return resp
