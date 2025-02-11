from src.schemas.response import UserSchema
from src.models.db import Users
from src.exc.exceptions import ParentException


def userview(func):

    async def wrapper(*args):
        original = await func(*args)
        if original:
            if isinstance(original, list):
                vlst = []
                for usr in original:
                    if isinstance(usr, Users):
                        vlst.append(UserSchema(
                            user_id=usr.user_id,
                            username=usr.username,
                            avatar=usr.avatar,
                            green_scores=usr.green_scores,
                            green_points=usr.green_points
                        ))
                return vlst[0] if len(vlst) == 1 else vlst
            else:
                raise ParentException
        else:
            return None
    return wrapper
