from src.service.core.posts import Posts


class FetchDataPostInteractor:
    @staticmethod
    async def get_by_id(post_id: int):
        return await Posts.get_by_id(post_id)

    @staticmethod
    async def get(filters):
        return await Posts.get(filters)
