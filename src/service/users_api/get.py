from src.service.core.users import Users


class FetchDataUserInteractor:
    @staticmethod
    async def get_user(user_id: int) -> Users:
        return await Users.get_user(user_id)
