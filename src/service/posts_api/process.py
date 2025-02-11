from src.service.core.posts import Posts


class ProcessDataPostInteractor:
    @staticmethod
    async def add_post(post, user_id):
        return await Posts.add(post, user_id)

    @staticmethod
    async def remove_post(post_id):
        return await Posts.delete(post_id)
