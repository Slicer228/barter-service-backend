from sqlalchemy import select, insert
from src.service.users_api.get import FetchDataUserInteractor
from src.exc.exceptions import ParentException, UserNotFound, PostNotFound
from src.models.db import UserPosts, PostPhotos, Categories, PostCategories, UserTrades, Trades
from src.schemas.request import AddPostSchema
from src.service.core.posts.filter import PostFilter
from src.service.core.utils_dao import category_exists
from src.service.db import async_session_maker
from src.service.dto.posts import postview
from src.service.core.enums import TradeTypes


@postview
async def get(session, filters):
    stmt = select(UserPosts.post_id)
    stmt = await PostFilter.affect_filters_to_stmt(stmt, filters)
    data = (await session.execute(stmt)).all()
    return [await get_post_by_id(session, post.post_id) for post in data]


async def get_post_by_id(session, post_id: int):
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
    stmt = select(UserTrades.user_id).where(UserTrades.post_id == post_id, UserTrades.utType == TradeTypes.POST.value)
    usr_id = await session.execute(stmt)
    usr_id = usr_id.scalars().first()
    if not usr_id:
        raise PostNotFound()
    user = await FetchDataUserInteractor.get_user(usr_id)
    return post, photos, categories, user


@postview
async def add(session, post: AddPostSchema, user_id: int) -> int | list[int]:
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
            utType=TradeTypes.POST.value)
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
        return [post_id]
    except BaseException as e:
        await session.rollback()
        raise e

