from src.service.dto.offers import offerView



class Offers:

    @staticmethod
    @offerView
    async def get_incoming(user_id: int):
        pass

    @staticmethod
    @offerView
    async def get_processing(user_id: int):
        pass

    @staticmethod
    @offerView
    async def get_outgoing(user_id: int):
        pass

    @staticmethod
    @offerView
    async def get_archive(user_id: int):
        pass