from src.utils import addLogAsync
from fastapi import APIRouter
from typing import Optional
from src.models.responseClasses import SchemaPost
from src.service.dao.posts import Posts

getPostsRouter = APIRouter(prefix="/posts")


@getPostsRouter.get("/posts/{post_id}")
async def get_posts(post_id: int) -> list[SchemaPost] | SchemaPost:
    res = await Posts.get([1,2,3,4,5,6])
    return res