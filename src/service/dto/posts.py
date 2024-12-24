from src.models.responseClasses import SchemaPost, SchemaPostPhoto, SchemaUser
from src.error_handlers import error_handler_posts


def postview(func):

    async def wrapper(*args):
        original = await func(*args)
        if original:
            if isinstance(original,list):
                psts_final = []
                for post in original:
                    photos = [SchemaPostPhoto(post_photo_name=i.post_photo_name, post_photo=i.post_photo) for i in post[1]]
                    owner = SchemaUser(user_id = post[3].user_id,
                                       avatar = post[3].avatar,
                                       username = post[3].username,
                                       green_scores=post[3].green_scores,
                                       green_points=post[3].green_points
                                       )
                    psts_final.append(SchemaPost(
                        owner=owner,
                        post_id=post[0].post_id,
                        post_name=post[0].post_name,
                        post_description=post[0].post_description,
                        post_type=post[0].post_type,
                        status=post[0].status,
                        photos=photos,
                        categories=post[2]
                    ))
                return psts_final
            else:
                return original
        else:
            return None
    return wrapper