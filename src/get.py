from src.utils import addLogAsync
from mysql.connector import Error
from src.conn import cursor
from fastapi import APIRouter
from src.classes import Post

getRouter = APIRouter()

@getRouter.get("/getUserData/{user_id}")
async def getUser(user_id: str):
    query = f"SELECT * FROM users WHERE user_id = '{user_id}'"
    try:
        await cursor.execute(query)
        data = await cursor.fetchall()
        resp = {'user_id': data[0][0], 'username': data[0][1], 'green_scores': data[0][2], 'green_points': data[0][3]}
        return resp
    except Error as e:
        await addLogAsync(e)
        return {"status": 0}


@getRouter.get("/getUserPosts/{user_id}")
async def get_posts(user_id: str):
    try:
        query = f"SELECT up.post_id FROM user_trades ut1 JOIN user_trades ut2 ON ut1.trade_id = ut2.trade_id JOIN user_posts up ON ut1.post_id = up.post_id WHERE ut1.user_id = '{user_id}' AND ut1.utType = 'post'"
        await cursor.execute(query)
        user_trades = await cursor.fetchall()
        user_trades = list(set(map(lambda x: x[0], user_trades)))
        resp = []
        for post_id in user_trades:
            post = await get_post(post_id)
            resp.append(post)
        return resp
    except Error as e:
        await addLogAsync(e)
        return {'status': 0}


@getRouter.get("/getPost/{post_id}")
async def get_post(post_id: int):
    query = f"SELECT * FROM user_posts WHERE post_id = {post_id}"
    await cursor.execute(query)
    postData = await cursor.fetchall()
    postData = postData[0]
    photos = []
    query = f"SELECT * FROM post_photos WHERE post_id = {post_id}"
    await cursor.execute(query)
    photosData = await cursor.fetchall()
    for photo in photosData:
        photos.append(photo[0])
    categories = []
    query = f"SELECT * FROM post_categories WHERE post_id = {post_id} ORDER BY category_type"
    await cursor.execute(query)
    categoriesData = await cursor.fetchall()
    for cat in categoriesData:
        categories.append(cat[1])
    return Post(post_id=postData[0], post_name=postData[1], post_description=postData[2], post_type=postData[3],
            status=postData[5], trade_id=postData[4], photos=photos, categories=categories)


@getRouter.get("/getUserIncomingPosts/{user_id}")
async def get_archive_posts(user_id: str):
    try:
        query = f"SELECT up.post_id FROM user_trades ut1 JOIN user_trades ut2 ON ut1.trade_id = ut2.trade_id JOIN user_posts up ON ut1.post_id = up.post_id WHERE ut1.user_id = '{user_id}' AND ut1.utType = 'post' AND ut2.utType = 'offer' AND up.status = 'active'"
        await cursor.execute(query)
        user_trades = await cursor.fetchall()
        user_trades = list(set(map(lambda x: x[0], user_trades)))
        resp = []
        for post_id in user_trades:
            post = await get_post(post_id)
            resp.append(post)
        return resp
    except Error as e:
        await addLogAsync(e)
        return {'status': 0}


@getRouter.get("/getUserArchivePosts/{user_id}")
async def get_archive_posts(user_id: str):
    try:
        query = f"SELECT up.post_id FROM user_trades ut1 JOIN user_trades ut2 ON ut1.trade_id = ut2.trade_id JOIN user_posts up ON ut1.post_id = up.post_id WHERE ut1.user_id = '{user_id}' AND ut1.utType = 'post' AND ut2.utType = 'offer' AND up.status = 'archive'"
        await cursor.execute(query)
        user_trades = await cursor.fetchall()
        user_trades = list(set(map(lambda x: x[0], user_trades)))
        resp = []
        for post_id in user_trades:
            post = await get_post(post_id)
            resp.append(post)
        return resp
    except Error as e:
        await addLogAsync(e)
        return {'status': 0}


@getRouter.get("/getUserProcessPosts/{user_id}")
async def get_process_posts(user_id: str):
    try:
        query = f"SELECT up.post_id FROM user_trades ut1 JOIN user_trades ut2 ON ut1.trade_id = ut2.trade_id JOIN user_posts up ON ut1.post_id = up.post_id WHERE ut1.user_id = '{user_id}' AND ut1.utType = 'post' AND ut2.utType = 'offer' AND up.status = 'process'"
        await cursor.execute(query)
        user_trades = await cursor.fetchall()
        user_trades = list(set(map(lambda x: x[0], user_trades)))
        resp = []
        for post_id in user_trades:
            post = await get_post(post_id)
            resp.append(post)
        return resp
    except Error as e:
        await addLogAsync(e)
        return {'status': 0}


@getRouter.get("/getAllPosts/")
async def get_all_posts():
    try:
        query = f"SELECT p.post_id FROM user_trades INNER JOIN user_posts p USING(post_id) WHERE user_trades.utType = 'post' and p.status = 'active'"
        await cursor.execute(query)
        allPosts = await cursor.fetchall()
        allPosts = list(set(map(lambda x: x[0], allPosts)))
        resp = []
        for post_id in allPosts:
            post = await get_post(post_id)
            resp.append(post)
        return resp
    except Error as e:
        await addLogAsync(e)
        return {'status': 0}
