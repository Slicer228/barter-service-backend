from src.utils import addLogAsync
from fastapi import APIRouter


postPostsRouter = APIRouter(prefix="/posts")


@postPostsRouter.post("/add/", response_model=SchemaPost)
async def create_post(post: SchemaAddPost = Depends()):
    try:
        await cursor.execute('START TRANSACTION')
        query = 'INSERT INTO trades (date) VALUES(Now());SELECT LAST_INSERT_ID();'
        await cursor.execute(query)
        trade_id = await cursor.fetchall
        trade_id = trade_id[0][0]
        query = f"INSERT INTO user_posts (post_name,post_description,post_type,trade_id,status) VALUES('{post.post_name}','{post.post_description}','{post.post_type}','{trade_id}','{post.status}');SELECT LAST_INSERT_ID();"
        await cursor.execute(query)
        post_id = await cursor.fetchall()
        post_id = post_id[0][0]
        await connection.commit()
        query = f"INSERT INTO user_trades(user_id,post_id,trade_id,utType) VALUES('{post.user_id}',{post_id},{trade_id},'post')"
        await cursor.execute(query)
        await connection.commit()
        if post.photos:
            for photo in post.photos:
                query = f"INSERT INTO post_photos(post_id,post_photo) VALUES({post_id},{photo})"
                await cursor.execute(query)
                await connection.commit()
        if post.categories:
            i = 0
            for cat in post.categories:
                query = f"INSERT INTO post_photos(post_id,category_id,category_type) VALUES({post_id},{cat},'{'secondary' if i else 'main'}')"
                i = 1
                await cursor.execute(query)
                await connection.commit()
        await cursor.execute('COMMIT')
        return SchemaPost(
            post_id=post_id,
            post_name=post_name,
            post_description=post_description,
            post_type=post_type,
            photos=photos,
            categories=categories,
            trade_id=trade_id,
            status='active'
        )
    except Error as e:
        await addLogAsync(e)
        return {"post": post,"status": 1}