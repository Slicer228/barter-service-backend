from fastapi import APIRouter
from src.utils import addLogAsync


postOffersRouter = APIRouter(prefix="/offers")

@postOffersRouter.post("/send/",response_model=SchemaPost)
async def send(data: SchemaActOffer = Depends()):
    try:
        query = f"SELECT user_trades.trade_id FROM user_trades WHERE post_id = {data.post_id} and utType = 'post'"
        await cursor.execute(query)
        trade_id = await cursor.fetchall()
        trade_id = trade_id[0][0]
        query = f"SELECT status FROM user_posts WHERE post_id = {data.post_id}"
        await cursor.execute(query)
        status = await cursor.fetchall()
        status = status[0][0]
        if data.user_id:
            query = f"INSERT INTO user_trades(user_id,post_id,trade_id,utType) VALUES('{data.user_id}',{data.source_post_id},{trade_id},'offer')"
            await cursor.execute(query)
            await connection.commit()
        post = await get_post(data.post_id)
        return post
    except Error as e:
        await addLogAsync(e)
        return {"status": 1}


@postOffersRouter.post("/reject/")
async def reject(data: SchemaActOffer = Depends()):
    try:
        query = f"SELECT user_trades.trade_id FROM user_trades WHERE post_id = {data.post_id} and utType = 'post'"
        await cursor.execute(query)
        trade_id = await cursor.fetchall()[0][0]
        query = f"DELETE from user_trades WHERE utType = 'offer' and trade_id = {trade_id} and post_id = {data.source_post_id}"
        await connection.commit()
        return {"status": 0}
    except Error as e:
        await addLogAsync(e)
        return {"status": 1}


@postOffersRouter.post("/accept/")
async def accept(data: SchemaActOffer = Depends()):
    try:
        query = f"SELECT user_trades.trade_id FROM user_trades WHERE post_id = {data.post_id} and utType = 'post'"
        await cursor.execute(query)
        trade_id = await cursor.fetchall()[0][0]
        query = f"DELETE from user_trades WHERE utType = 'offer' and trade_id = {trade_id} and post_id <> {data.source_post_id}"
        await connection.commit()
        query = f"UPDATE user_posts SET status = 'process' WHERE post_id = {data.post_id}"
        await cursor.execute(query)
        await connection.commit()
        return {"status": 0}
    except Error as e:
        await addLogAsync(e)
        return {"status": 1}


@postOffersRouter.post("/end/")
async def end(data: SchemaActOffer = Depends()):
    try:
        query = f"UPDATE user_posts SET status = 'archive' WHERE post_id = {data.post_id}"
        await cursor.execute(query)
        await connection.commit()
        query = f"UPDATE user_posts SET status = 'archive' WHERE post_id = {data.source_post_id}"
        await cursor.execute(query)
        await connection.commit()
        query = f"DELETE FROM user_trades WHERE post_id = {data.post_id}"
        await cursor.execute(query)
        await connection.commit()
        query = f"DELETE FROM user_trades WHERE post_id = {data.source_post_id}"
        await cursor.execute(query)
        await connection.commit()

        return {"status": 0}
    except Error as e:
        await addLogAsync(e)
        return {"status": 1}