from src.service.utils import add_log
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.cors import origins
import uvicorn
from contextlib import asynccontextmanager
from src.routers.posts.post import router as post_post_router
from src.routers.posts.get import router as get_post_router
from src.routers.users.get import router as get_users_router
from src.routers.auth import router as auth_router
from src.routers.trades.get import router as get_trades_router
from src.routers.trades.post import router as post_trades_router
from dotenv import load_dotenv
from src.exc.exception_handlers import constructors

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.include_router(post_post_router)
        app.include_router(get_post_router)
        app.include_router(get_users_router)
        app.include_router(auth_router)
        app.include_router(get_trades_router)
        app.include_router(post_trades_router)

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

