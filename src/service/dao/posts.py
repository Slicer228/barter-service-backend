from src.service.dto.posts import postview
from src.models.paramClasses import SchemaAddPost
from src.models.dbModels import User_trades, User_posts, Post_photos, Post_categories, Categories, Trades
from src.service.dao.users import User
from sqlalchemy import select, insert
from src.db import async_session_maker
from src.routers.responses import PostResponse


class Posts:

    @staticmethod
    async def delete(post_id: int):
        pass

    @staticmethod
    @postview
    async def add(post: SchemaAddPost | list[SchemaAddPost]):
        if isinstance(post, list):
            pass
        else:
            stmt1 = insert(Trades)
            async with async_session_maker() as session:
                async with session.begin():
                    data = await session.execute(stmt1)
                    await session.commit()
                    trade_id = data.lastrowid
                async with session.begin():
                    stmt2 = insert(User_posts).values(
                        post_name = post.post_name,
                        post_type = post.post_type,
                        trade_id = trade_id,
                        post_description = post.post_description
                    )
                    data = await session.execute(stmt2)
                    await session.commit()
                    post_id = data.lastrowid

                stmt = insert(User_trades).values(
                    user_id=post.user_id,
                    post_id=post_id,
                    trade_id=trade_id,
                    utType='post')
                await session.execute(stmt)
                await session.commit()

                if post.categories:
                    i = 0
                    for cat in post.categories:
                        stmt = insert(Post_categories).values(
                            post_id = post_id,
                            category_id = cat,
                            category_type = 'main' if not i else 'secondary')
                        i = 1
                        await session.execute(stmt)
                        await session.commit()
                if post.photos:
                    for photo in post.photos:
                        stmt = insert(Post_photos).values(post_photo=photo.post_photo,post_photo_name=photo.post_photo_name, post_id=post_id)
                        await session.execute(stmt)
                        await session.commit()

                return post_id



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
    async def get(post_id: int | list[int], user_id: int | list[int] | None = None):
        user = None
        if isinstance(post_id, list):
            psts = []
            if user_id:
                async with async_session_maker() as session:
                    for p,u in zip(post_id,user_id):
                        stmtP = select(User_posts).where(User_posts.post_id == p)
                        stmtPP = select(Post_photos.post_photo_name, Post_photos.post_photo).where(Post_photos.post_id == p)
                        stmtC = select(Categories.category_name).join(Post_categories.category_names).order_by(Post_categories.category_type)
                        user = await User.get_user(u)
                        post = await session.execute(stmtP)
                        post = post.scalars().first()
                        photos = await session.execute(stmtPP)
                        photos = photos.scalars().all()
                        categories = await session.execute(stmtC)
                        categories = categories.scalars().all()
                        psts.append((post,photos,categories,user))
            else:
                async with async_session_maker() as session:
                    for p in post_id:
                        stmtP = select(User_posts).where(User_posts.post_id == p)
                        stmtPP = select(Post_photos.post_photo_name,Post_photos.post_photo).where(Post_photos.post_id == p)
                        stmtC = select(Categories.category_name).join(Post_categories.category_names).order_by(Post_categories.category_type)
                        stmt = select(User_trades.user_id).where(User_trades.post_id == p,User_trades.utType == 'post')
                        usr_id = await session.execute(stmt)
                        usr_id = usr_id.scalars().first()
                        user = await User.get_user(usr_id)
                        post = await session.execute(stmtP)
                        post = post.scalars().first()
                        photos = await session.execute(stmtPP)
                        photos = photos.scalars().all()
                        categories = await session.execute(stmtC)
                        categories = categories.scalars().all()
                        if not isinstance(user,dict) and post:
                            psts.append((post,photos,categories,user))
            return psts if psts else PostResponse.NOT_FOUND
        else:
            stmtP = select(User_posts).where(User_posts.post_id == post_id)
            stmtPP = select(Post_photos.post_photo_name, Post_photos.post_photo).where(Post_photos.post_id == post_id)
            stmtC = select(Categories.category_name).join(Post_categories.category_names).where(Post_categories.post_id == post_id).order_by(Post_categories.category_type)
            async with async_session_maker() as session:
                post = await session.execute(stmtP)
                post = post.scalars().first()
                photos = await session.execute(stmtPP)
                photos = photos.scalars().all()
                categories = await session.execute(stmtC)
                categories = categories.scalars().all()
                if user_id:
                    user = await User.get_user(user_id)
                else:
                    stmt = select(User_trades.user_id).where(User_trades.post_id == post_id,User_trades.utType == 'post')
                    usr_id = await session.execute(stmt)
                    usr_id = usr_id.scalars().first()
                    user = await User.get_user(usr_id)
                return (post,photos,categories,user)