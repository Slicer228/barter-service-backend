from src.service.dto.posts import postview
from src.models.paramClasses import SchemaAddPost
from src.models.dbModels import User_trades, User_posts, Post_photos, Post_categories, Categories, Trades
from src.service.dao.users import User
from sqlalchemy import select, insert
from src.db import async_session_maker
from src.internal_exceptions import NoAccess, NotFound

class Posts:

    @staticmethod
    async def delete(post_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                try:
                    pass
                finally:
                    await session.rollback()

    @staticmethod
    @postview
    async def add(post: SchemaAddPost | list[SchemaAddPost], user_id: int) -> int | list[int]:

        async def add_one(post: SchemaAddPost) -> int:
            nonlocal user_id
            async with async_session_maker() as session:
                async with session.begin():
                    try:
                        stmt1 = insert(Trades)
                        data = await session.execute(stmt1)
                        trade_id = data.lastrowid
                        stmt2 = insert(User_posts).values(
                            post_name=post.post_name,
                            post_type=post.post_type,
                            trade_id=trade_id,
                            post_description=post.post_description
                        )
                        data = await session.execute(stmt2)

                        post_id = data.lastrowid

                        stmt = insert(User_trades).values(
                            user_id=user_id,
                            post_id=post_id,
                            trade_id=trade_id,
                            utType='post')
                        await session.execute(stmt)

                        if post.categories:
                            i = 0
                            for cat in post.categories:
                                stmt = insert(Post_categories).values(
                                    post_id=post_id,
                                    category_id=cat,
                                    category_type='main' if not i else 'secondary')
                                i = 1
                                await session.execute(stmt)

                        if post.photos:
                            for photo in post.photos:
                                stmt = insert(Post_photos).values(post_photo=bytes(photo.post_photo, 'utf8'),
                                                                  post_photo_name=photo.post_photo_name,
                                                                  post_id=post_id)
                                await session.execute(stmt)

                        await session.commit()
                        return post_id
                    finally:
                        await session.rollback()

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
    async def get(post_id: int | list[int]):

        async def get_one(post_id: int) -> tuple:
            stmtP = select(User_posts).where(User_posts.post_id == post_id)
            stmtPP = select(Post_photos).where(Post_photos.post_id == post_id)
            stmtC = (select(Categories).join(Post_categories.category_names)
                .where(Post_categories.post_id == post_id)
                .order_by(Post_categories.category_type))
            async with async_session_maker() as session:
                post = await session.execute(stmtP)
                post = post.scalars().first()
                photos = await session.execute(stmtPP)
                photos = photos.scalars().all()
                categories = await session.execute(stmtC)
                categories = categories.scalars().all()
                stmt = select(User_trades.user_id).where(User_trades.post_id == post_id, User_trades.utType == 'post')
                usr_id = await session.execute(stmt)
                usr_id = usr_id.scalars().first()
                try:
                    user = await User.get_user(usr_id)
                    return (post, photos, categories, user)
                except BaseException:
                    pass

        if isinstance(post_id, list):
            psts = []
            for pst in post_id:
                psts.append(await get_one(pst))
            return psts
        else:
            pst = await get_one(post_id)
            return [pst] if pst else []