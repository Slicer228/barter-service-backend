import configparser
from src.utils import addLogAsync
import aiomysql


cfg = configparser.ConfigParser()
cfg.read('config.ini')

connection = None
cursor = None

async def conn():
    global connection,cursor
    try:
        connection = await aiomysql.connect(
            host=cfg["MySql"]["host"],
            user=cfg["MySql"]["username"],
            password=cfg["MySql"]["password"],
            db=cfg["MySql"]["database"],
        )
        cursor = await connection.cursor()
    except Exception as e:
        await addLogAsync(e)

async def close_conn():
    global connection
    connection.close()


