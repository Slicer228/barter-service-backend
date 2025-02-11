from src.schemas.request import AddPostSchema
from src.service.db import async_session_maker
from src.service.core.posts import dao
from src.service.dto.posts import postview


async def delete(post_id: int):
    async with async_session_maker() as session:
        async with session.begin():
            try:
                pass
            except BaseException as e:
                await session.rollback()
                raise e


@postview
async def get_by_id(post_id: int):
    if post_id == 0:
        return []
    else:
        async with async_session_maker() as session:
            async with session.begin():
                pst = await dao.get_post_by_id(session, post_id)
                return [pst] if pst else []


async def add(post: AddPostSchema, user_id: int):
    async with async_session_maker() as session:
        async with session.begin():
            post_id = await dao.add(session, post, user_id)
            return post_id


async def get(filters):
    async with async_session_maker() as session:
        return await dao.get(session, filters)
