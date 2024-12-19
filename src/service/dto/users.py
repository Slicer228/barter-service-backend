from src.models.responseClasses import SchemaUser
from src.error_handlers import error_handler_users


def userview(func):
    @error_handler_users
    async def wrapper(*args):
        original = await func(*args)
        if original:
            if isinstance(original,list):
                vlst = []
                for usr in original:
                    vlst.append(SchemaUser(
                        user_id=usr.user_id,
                        username=usr.username,
                        avatar=usr.avatar,
                        green_scores=usr.green_scores,
                        green_points=usr.green_points
                    ))
                return vlst
            else:
                return SchemaUser(
                    user_id=original.user_id,
                    username=original.username,
                    avatar=original.avatar,
                    green_scores=original.green_scores,
                    green_points=original.green_points
                )
        else:
            return None
    return wrapper