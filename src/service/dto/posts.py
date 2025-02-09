from src.schemas.response import SchemaPost, SchemaPostPhoto, SchemaUser


def postview(func):

    async def wrapper(*args):
        original: list[int] | list[tuple] = await func(*args)
        if original:
            if isinstance(original, list):
                psts_final = []
                for post in original:
                    if isinstance(post, tuple):
                        photos = [SchemaPostPhoto(post_photo_name=i.post_photo_name, post_photo=i.post_photo) for i in post[1]]
                        owner = SchemaUser(user_id = post[3].user_id,
                                           avatar = post[3].avatar,
                                           username = post[3].username,
                                           green_scores=post[3].green_scores,
                                           green_points=post[3].green_points
                                           )
                        categories = [i.category_id for i in post[2]]

                        psts_final.append(SchemaPost(
                            owner=owner,
                            post_id=post[0].post_id,
                            trade_id=post[0].trade_id,
                            post_name=post[0].post_name,
                            post_description=post[0].post_description,
                            post_type=post[0].post_type,
                            status=post[0].trade_status,
                            photos=photos,
                            categories=categories
                        ))
                    elif isinstance(post,int):
                        return original[0] if len(original) == 1 else original
                return psts_final[0] if len(psts_final) == 1 else psts_final
            else:
                return original
        else:
            return None
    return wrapper