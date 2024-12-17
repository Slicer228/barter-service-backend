from src.utils import addLogAsync
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.networkCfg import origins
import uvicorn
from contextlib import asynccontextmanager
from src.routers.posts.post import postPostsRouter
from src.routers.posts.get import getPostsRouter
from src.routers.users.get import getUsersRouter
from src.routers.users.post import postUsersRouter
#from src.routers.offers.get import getOffersRouter
#from src.routers.offers.post import postOffersRouter
from dotenv import load_dotenv


load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.include_router(postPostsRouter)
        app.include_router(getPostsRouter)
        app.include_router(getUsersRouter)
        app.include_router(postUsersRouter)
        #app.include_router(getOffersRouter)
        #app.include_router(postOffersRouter)

        yield
        print('end')
    except Exception as e:
        await addLogAsync(e)

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)

