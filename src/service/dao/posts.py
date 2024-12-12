from src.service.dto.posts import postview
from src.models.paramClasses import SchemaAddPost
from src.models.dbModels import User_trades, User_posts, Post_photos, Post_categories, Categories
from src.service.dao.users import User
from sqlalchemy import select
from src.db import async_session_maker


class Posts:

    @staticmethod
    async def delete(post_id: int):
        pass

    @staticmethod
    @postview
    async def add(post: SchemaAddPost):
        pass

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
                        psts.append((post,photos,categories,user))
            return psts
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