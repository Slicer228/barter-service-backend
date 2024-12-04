from src.utils import addLogAsync
from mysql.connector import Error
from src.conn import cursor, connection
from src.classes import User,Post
from fastapi import APIRouter


postRouter = APIRouter()


@postRouter.post("/add_user/")
async def create_user(user: User):
    query = f"INSERT INTO users (user_id, username, green_scores) VALUES('{user.user_id}','{user.username}',0)"
    try:
        await cursor.execute(query)
        await connection.commit()
        return {"status": 0}
    except Error as e:
        await addLogAsync(e)
        return {"status": 1}


@postRouter.post("/add_post/")
async def create_post(user_id: str, post: Post):
    try:
        await cursor.execute('START TRANSACTION')
        query = 'INSERT INTO trades (date) VALUES(Now());SELECT LAST_INSERT_ID();'
        await cursor.execute(query)
        post.trade_id = await cursor.fetchall[0][0]
        query = f"INSERT INTO user_posts (post_name,post_description,post_type,trade_id,status) VALUES('{post.post_name}','{post.post_description}','{post.post_type}','{post.trade_id}','{post.status}');SELECT LAST_INSERT_ID();"
        await cursor.execute(query)
        post.post_id = await cursor.fetchall()[0][0]
        await connection.commit()
        query = f"INSERT INTO user_trades(user_id,post_id,trade_id,utType) VALUES('{user_id}',{post.post_id},{post.trade_id},'post')"
        await cursor.execute(query)
        await connection.commit()
        if post.photos:
            for photo in post.photos:
                query = f"INSERT INTO post_photos(post_id,post_photo) VALUES({post.post_id},{photo})"
                await cursor.execute(query)
                await connection.commit()
        if post.categories:
            i = 0
            for cat in post.categories:
                query = f"INSERT INTO post_photos(post_id,category_id,category_type) VALUES({post.post_id},{cat},'{'secondary' if i else 'main'}')"
                i = 1
                await cursor.execute(query)
                await connection.commit()
        await cursor.execute('COMMIT')
        return {"post": post,"status": 0}
    except Error as e:
        await addLogAsync(e)
        return {"post": post,"status": 1}


@postRouter.post("/send_offer/")
async def send_offer(user_id: str, post_id: int, source_post_id: int):
    try:
        query = f"SELECT user_trades.trade_id FROM user_trades WHERE post_id = {post_id} and utType = 'post'"
        await cursor.execute(query)
        trade_id = await cursor.fetchall()[0][0]
        query = f"SELECT status FROM user_posts WHERE post_id = {post_id}"
        await cursor.execute(query)
        status = await cursor.fetchall()[0][0]
        query = f"INSERT INTO user_trades(user_id,post_id,trade_id,utType) VALUES('{user_id}',{source_post_id},{trade_id},'offer')"
        await cursor.execute(query)
        await connection.commit()
        return {"status": 0}
    except Error as e:
        await addLogAsync(e)
        return {"status": 1}


@postRouter.post("/reject_offer/")
async def reject_offer(source_post_id: int, post_id: int):
    try:
        query = f"SELECT user_trades.trade_id FROM user_trades WHERE post_id = {post_id} and utType = 'post'"
        await cursor.execute(query)
        trade_id = await cursor.fetchall()[0][0]
        query = f"DELETE from user_trades WHERE utType = 'offer' and trade_id = {trade_id} and post_id = {source_post_id}"
        await connection.commit()
        return {"status": 0}
    except Error as e:
        await addLogAsync(e)
        return {"status": 1}


@postRouter.post("/accept_offer/")
async def accept_offer(source_post_id: int, post_id: int):
    try:
        query = f"SELECT user_trades.trade_id FROM user_trades WHERE post_id = {post_id} and utType = 'post'"
        await cursor.execute(query)
        trade_id = await cursor.fetchall()[0][0]
        query = f"DELETE from user_trades WHERE utType = 'offer' and trade_id = {trade_id} and post_id <> {source_post_id}"
        await connection.commit()
        query = f"UPDATE user_posts SET status = 'process' WHERE post_id = {post_id}"
        await cursor.execute(query)
        await connection.commit()
        return {"status": 0}
    except Error as e:
        await addLogAsync(e)
        return {"status": 1}


@postRouter.post("/end_offer/")
async def end_offer(post_id: int, source_post_id: int):
    try:
        query = f"UPDATE user_posts SET status = 'archive' WHERE post_id = {post_id}"
        await cursor.execute(query)
        await connection.commit()
        query = f"UPDATE user_posts SET status = 'archive' WHERE post_id = {source_post_id}"
        await cursor.execute(query)
        await connection.commit()
        query = f"DELETE FROM user_trades WHERE post_id = {post_id}"
        await cursor.execute(query)
        await connection.commit()
        query = f"DELETE FROM user_trades WHERE post_id = {source_post_id}"
        await cursor.execute(query)
        await connection.commit()

        return {"status": 0}
    except Error as e:
        await addLogAsync(e)
        return {"status": 1}