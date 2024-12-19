from src.utils import addLogAsync
from fastapi import APIRouter, HTTPException, Depends
from src.service.dao.posts import Posts
from src.models.responseClasses import SchemaPost
from src.models.paramClasses import SchemaAddPost

postPostsRouter = APIRouter(prefix="/posts")


@postPostsRouter.post("/add/", response_model=SchemaPost)
async def create_post(post: SchemaAddPost = Depends()):
    resp = await Posts.add(post)
    return resp