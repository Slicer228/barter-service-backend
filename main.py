from src.utils import addLogAsync
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.conn import conn,close_conn
from src.networkCfg import origins
import uvicorn
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await conn()
        from src.get import getRouter
        from src.post import postRouter
        app.include_router(getRouter)
        app.include_router(postRouter)

        yield
        await close_conn()
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
    uvicorn.run(app,host="127.0.0.1",port=8000)

