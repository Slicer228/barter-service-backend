from src.schemas.response_s import SchemaUser
from src.exception_handlers import error_handler_users
from src.models.dbModels import Users
from src.exceptions import ParentException


def userview(func):
    @error_handler_users
    async def wrapper(*args):
        original = await func(*args)
        if original:
            if isinstance(original, list):
                vlst = []
                for usr in original:
                    if isinstance(usr, Users):
                        vlst.append(SchemaUser(
                            user_id=usr.user_id,
                            username=usr.username,
                            avatar=usr.avatar,
                            green_scores=usr.green_scores,
                            green_points=usr.green_points
                        ))
                return vlst[0] if len(vlst) == 1 else vlst
            else:
                raise ParentException('user dao error!')
        else:
            return None
    return wrapper
