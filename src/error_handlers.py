from src.routers.responses import UserResponse, PostResponse
from sqlalchemy.exc import IntegrityError
from src.errors import NotFound, AuthError, UserAlreadyExists
from fastapi import HTTPException
from src.utils import addLog


def error_handler_users(func):
    async def wrapper(*args):
        try:
            result = await func(*args)
            return result
        except IntegrityError:
            raise HTTPException(**UserResponse.ALREADY_EXISTS)
        except NotFound:
            raise HTTPException(**UserResponse.NOT_FOUND)
        except AuthError:
            raise HTTPException(**UserResponse.NOT_AUTH)
        except UserAlreadyExists:
            raise HTTPException(**UserResponse.ALREADY_EXISTS)
        except Exception as e:
            await addLog(e)
            raise HTTPException(**UserResponse.ERROR)

    return wrapper

def error_handler_posts(func):
    async def wrapper(*args):
        try:
            result = await func(*args)
            return result
        except IntegrityError:
            raise HTTPException(**UserResponse.NOT_FOUND)
        except NotFound:
            raise HTTPException(**PostResponse.NOT_FOUND)
        except AuthError:
            raise HTTPException(**UserResponse.NOT_AUTH)
        except Exception as e:
            await addLog(e)
            raise HTTPException(**PostResponse.ERROR)

    return wrapper