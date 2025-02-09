from src.service.utils import add_log
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.cors import origins
import uvicorn
from contextlib import asynccontextmanager
from routers.posts.post import router as post_post_router
from routers.posts.get import router as get_post_router
from routers.users.get import router as get_users_router
from routers.auth import router as auth_router
from routers.offers.get import router as get_offers_router
from routers.offers.post import router as post_offers_router
from dotenv import load_dotenv
from src.service.exception_handlers import constructors

load_dotenv()
from sqlalchemy import select
from src.models.db import UserTrades, UserPosts, Categories, PostCategories
from src.service.db import async_session_maker
import asyncio
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.include_router(post_post_router)
        app.include_router(get_post_router)
        app.include_router(get_users_router)
        app.include_router(auth_router)
        app.include_router(get_offers_router)
        app.include_router(post_offers_router)

        yield

        print('end')
    except Exception as e:
        await add_log(e)

app = FastAPI(lifespan=lifespan)


for exc_construct in constructors:
    app.add_exception_handler(*exc_construct)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)

