from src.routers.responses import UserResponse, PostResponse
from sqlalchemy.exc import IntegrityError
from src.errors import NotFound
from fastapi import HTTPException


def error_handler_users(func):
    async def wrapper(*args):
        try:
            result = await func(*args)
            return result
        except IntegrityError:
            raise HTTPException(**UserResponse.ALREADY_EXISTS)
        except NotFound:
            raise HTTPException(**UserResponse.NOT_FOUND)
        except Exception:
            raise HTTPException(**UserResponse.ERROR)

    return wrapper

def error_handler_posts(func):
    async def wrapper(*args):
        try:
            result = await func(*args)
            return result
        except NotFound:
            raise HTTPException(**PostResponse.NOT_FOUND)
        except Exception:
            raise HTTPException(**PostResponse.ERROR)

    return wrapper