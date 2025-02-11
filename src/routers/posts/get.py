from fastapi import APIRouter
from src.schemas.response import PostSchema
from src.service.posts_api.get import FetchDataPostInteractor
from src.schemas.filters import PostFilterSchema


router = APIRouter(prefix="/posts")


@router.get("/{post_id}")
async def get_post_by_id_(post_id: int) -> list[PostSchema] | PostSchema | None:
    resp = await FetchDataPostInteractor.get_by_id(post_id)
    return resp


@router.post("/")
async def get_posts(filters: PostFilterSchema) -> list[PostSchema] | PostSchema | None:
    resp = await FetchDataPostInteractor.get(filters)
    return resp
