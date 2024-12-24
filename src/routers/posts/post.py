from src.utils import addLog
from fastapi import APIRouter, HTTPException, Depends
from src.service.dao.posts import Posts
from src.models.responseClasses import SchemaPost
from src.models.paramClasses import SchemaAddPost

postPostsRouter = APIRouter(prefix="/posts")


@postPostsRouter.post("/add/")
async def create_post(post: SchemaAddPost) -> int:
    resp = await Posts.add(post)
    return resp
