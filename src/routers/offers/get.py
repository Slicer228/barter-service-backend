from fastapi import APIRouter
from src.utils import addLog


getOffersRouter = APIRouter(prefix="/offers")


@getOffersRouter.get("/outgoing/{user_id}", response_model=list[SchemaOffer])
async def get_outgoing(user_id: str):
    pass

@getOffersRouter.get("/incoming/{user_id}", response_model=list[SchemaOffer])
async def get_incoming(user_id: str):
    try:
        query = f"SELECT t.trade_id, up.post_id FROM trades t INNER JOIN user_posts up ON t.trade_id = up.trade_id AND up.status = 'active' INNER JOIN user_trades ut USING(post_id) WHERE ut.utType = 'post' AND ut.user_id = '{user_id}'"
        await cursor.execute(query)
        user_trades = await cursor.fetchall()
        resp = []
        for row in user_trades:
            query = f"SELECT ut.user_id, ut.post_id FROM user_trades ut WHERE ut.trade_id = {row[0]} and ut.utType = 'offer'"
            await cursor.execute(query)
            offers_from_users = await cursor.fetchall()
            for offer in offers_from_users:
                post = await get_post(row[1])
                source_post = await get_post(offer[1])
                from_user = await getUser(offer[0])
                resp.append(SchemaOffer(
                    post=post,
                    source_post=source_post,
                    from_user=from_user
                ))
        return resp
    except Error as e:
        await addLogAsync(e)
        return {'status': 0}


@getOffersRouter.get("/archive/{user_id}", response_model=list[SchemaPost])
async def get_archive(user_id: str):
    try:
        query = f"SELECT up.post_id FROM user_posts up INNER JOIN user_trades ut ON up.trade_id = ut.trade_id AND ut.user_id = '{user_id}' AND up.status = 'archive'"
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


@getOffersRouter.get("/process/{user_id}", response_model=list[SchemaPost])
async def get_process(user_id: str):
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