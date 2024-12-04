import logging,asyncio


logging.basicConfig(level=logging.ERROR,filename="logs.log",filemode="a",
format="%(asctime)s %(levelname)s %(message)s"
)

def addLog(err):
    logging.error(str(err))

async def addLogAsync(err):
    addLogTask = asyncio.create_task(addLog(err))
    await addLogTask