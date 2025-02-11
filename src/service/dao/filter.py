from src.schemas.filters import PostFilterSchema
from src.models.db import UserPosts, PostCategories
from sqlalchemy import or_, and_, func, all_, select


class BaseFilter:
    ...


class PostFilter(BaseFilter):

    @staticmethod
    async def _affect_category_filters(stmt, categories: list[int], flag):

        if not categories:
            return stmt

        if flag:
            subquery = \
                select(PostCategories.post_id)\
                .filter(PostCategories.category_id.in_(categories))\
                .group_by(PostCategories.post_id)\
                .having(func.count(PostCategories.category_id) == len(categories))\
                .subquery()

            new_stmt = \
                stmt.join(subquery, UserPosts.post_id == subquery.c.post_id)\
                .join(UserPosts.related_categories)\
                .group_by(UserPosts.post_id)\
                .having(func.count(PostCategories.category_id.distinct()) == len(categories))

        else:
            new_stmt = stmt.join(UserPosts.related_categories).where(
                PostCategories.category_id.in_(categories)
            )

        return new_stmt.distinct(UserPosts.post_id)

    @classmethod
    async def affect_filters_to_stmt(cls, stmt, filters: PostFilterSchema):
        return await cls._affect_category_filters(stmt, filters.categories, filters.categories_strict_flag)
