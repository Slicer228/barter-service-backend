from fastapi import APIRouter
from src.schemas.response import PostSchema
from src.service.posts_api.posts_api import Posts
from src.schemas.filters import PostFilterSchema


router = APIRouter(prefix="/posts")


@router.get("/{post_id}")
async def get_post_by_id_(post_id: int, filters: PostFilterSchema) -> list[PostSchema] | PostSchema | None:
    resp = await Posts.get_by_id(post_id)
    return resp


@router.post("/")
async def get_posts(filters: PostFilterSchema) -> list[PostSchema] | PostSchema | None:
    resp = await Posts.get(filters)
    return resp
