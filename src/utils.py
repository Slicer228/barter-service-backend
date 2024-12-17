import logging,asyncio


logging.basicConfig(level=logging.ERROR,filename="logs.log",filemode="a",
format="%(asctime)s %(levelname)s %(message)s"
)

async def addLogAsync(err):
    logging.error(str(err))
