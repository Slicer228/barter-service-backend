from src.service.dto.posts import postview
from src.schemas.request import AddPostSchema
from src.models.db import UserTrades, UserPosts, PostPhotos, PostCategories, Categories, Trades
from src.service.users_api import User
from sqlalchemy import select, insert
from src.service.db import async_session_maker
from src.exc.exceptions import ParentException
from src.service.core.utils_dao import category_exists
from src.service.core.posts.filter import PostFilter


class Posts:

    @staticmethod
    async def delete(post_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                except BaseException as e:
                    await session.rollback()
                    raise e

    @staticmethod
    @postview
    async def add(post: AddPostSchema | list[AddPostSchema], user_id: int) -> int | list[int]:

        async def add_one(post: AddPostSchema) -> int:
            nonlocal user_id
            async with async_session_maker() as session:
                async with session.begin():
                    try:
                        stmt1 = insert(Trades)
                        data = await session.execute(stmt1)
                        trade_id = data.lastrowid
                        stmt2 = insert(UserPosts).values(
                            post_name=post.post_name,
                            post_type=post.post_type,
                            trade_id=trade_id,
                            post_description=post.post_description
                        )
                        data = await session.execute(stmt2)

                        post_id = data.lastrowid

                        stmt = insert(UserTrades).values(
                            user_id=user_id,
                            post_id=post_id,
                            trade_id=trade_id,
                            utType='post')
                        await session.execute(stmt)

                        if post.categories:
                            i = 0
                            for cat in post.categories:
                                await category_exists(session, cat)
                                stmt = insert(PostCategories).values(
                                    post_id=post_id,
                                    category_id=cat,
                                    category_type='main' if not i else 'secondary')
                                i = 1
                                await session.execute(stmt)

                        if post.photos:
                            for photo in post.photos:
                                stmt = insert(PostPhotos).values(post_photo=bytes(photo.post_photo, 'utf8'),
                                                                 post_photo_name=photo.post_photo_name,
                                                                 post_id=post_id)
                                await session.execute(stmt)

                        await session.commit()
                        return post_id
                    except BaseException as e:
                        await session.rollback()
                        raise e

        if isinstance(post, list):
            posts = []
            for pst in post:
                posts.append(await add_one(pst))
            return posts
        else:
            return [await add_one(post)]

    @staticmethod
    async def get_all():
        pass

    @staticmethod
    async def get_all_user(user_id: str):
        pass

    @staticmethod
    async def get_archive_user(user_id: str):
        pass

    @staticmethod
    @postview
    async def _get_post_by_id(session, post_id: int):
        stmtP = select(UserPosts).where(UserPosts.post_id == post_id)
        stmtPP = select(PostPhotos).where(PostPhotos.post_id == post_id)
        stmtC = (select(Categories).join(PostCategories.category_names)
                 .where(PostCategories.post_id == post_id)
                 .order_by(PostCategories.category_type))
        post = await session.execute(stmtP)
        post = post.scalars().first()
        photos = await session.execute(stmtPP)
        photos = photos.scalars().all()
        categories = await session.execute(stmtC)
        categories = categories.scalars().all()
        stmt = select(UserTrades.user_id).where(UserTrades.post_id == post_id, UserTrades.utType == 'post')
        usr_id = await session.execute(stmt)
        usr_id = usr_id.scalars().first()
        try:
            user = await User.get_user(usr_id)
            return post, photos, categories, user
        except BaseException:
            raise ParentException('Error in getting user')

    @classmethod
    async def get_by_id(cls, post_id: int):
        if post_id == 0:
            return []
        else:
            async with async_session_maker() as session:
                pst = await cls._get_post_by_id(session, post_id)
                return [pst] if pst else []

    @classmethod
    @postview
    async def get(cls, filters):
        async with async_session_maker() as session:
            stmt = select(UserPosts.post_id)
            stmt = await PostFilter.affect_filters_to_stmt(stmt, filters)
            data = (await session.execute(stmt)).all()
            return [await cls._get_post_by_id(session, post.post_id) for post in data]