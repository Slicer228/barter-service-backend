from src.exceptions import *
from src.internal_exceptions import *
from sqlalchemy.exc import IntegrityError
from src.utils import addLog


def error_handler_users(func):
    async def wrapper(*args):
        try:
            result = await func(*args)
            return result
        except IntegrityError:
            raise UserAlreadyExists()
        except NotFound:
            raise UserNotFound()
        except AuthError:
            raise UserUnauthorized()
        except Exception as e:
            await addLog(e)
            raise ParentException()

    return wrapper


def error_handler_posts(func):
    async def wrapper(*args):
        try:
            result = await func(*args)
            return result
        except NotFound:
            raise PostNotFound()
        except NoAccess:
            raise PostBlocked()
        except Exception as e:
            await addLog(e)
            raise ParentException()
    return wrapper


def error_handler_offers(func):
    async def wrapper(*args):
        try:
            result = await func(*args)
            return result
        except BaseException as e:
            await addLog(e)
            raise ParentException()

    return wrapper
