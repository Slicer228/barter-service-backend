from src.models.responseClasses import SchemaPost, SchemaPostPhoto, SchemaPostCategories
from src.error_handlers import error_handler_posts


def postview(func):
    @error_handler_posts
    async def wrapper(*args):
        original = await func(*args)
        if original:
            if isinstance(original,list):
                psts_final = []
                for post in original:
                    photos = [SchemaPostPhoto(post_photo_name=i.post_photo_name, post_photo=i.post_photo) for i in post[1]]
                    categories = [SchemaPostCategories(category_name=i.category_name) for i in post[2]]
                    psts_final.append(SchemaPost(
                        owner=post[3],
                        post_id=post[0].post_id,
                        post_name=post[0].post_name,
                        post_description=post[0].post_description,
                        post_type=post[0].post_type,
                        status=post[0].status,
                        photos=photos,
                        categories=categories
                    ))
                return psts_final
            elif isinstance(original,SchemaPost):
                photos = [SchemaPostPhoto(post_photo_name = i.post_photo_name, post_photo = i.post_photo) for i in original[1]]
                categories = [SchemaPostCategories(category_name = i.category_name) for i in original[2]]
                post_final = SchemaPost(
                    owner = original[3],
                    post_id = original[0].post_id,
                    post_name = original[0].post_name,
                    post_description = original[0].post_description,
                    post_type = original[0].post_type,
                    status = original[0].status,
                    photos = photos,
                    categories = categories
                )
                return post_final
            else:
                return original
        else:
            return None
    return wrapper