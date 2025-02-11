from src.schemas.request import RegisterUserSchema


class ProcessDataUserInteractor:
    @staticmethod
    async def register_user(usrobj: RegisterUserSchema):
        return await ProcessDataUserInteractor.register_user(usrobj)
