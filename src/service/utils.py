import logging

logging.basicConfig(
    level=logging.ERROR,
    filename="logs.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s"
)


async def add_log(err):
    logging.error(str(err))

