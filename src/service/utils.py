import logging
from fastapi import Request, Depends
from jose import JWTError, jwt
from config import settings
from src.service.exceptions import UserUnauthorized

logging.basicConfig(
    level=logging.ERROR,
    filename="logs.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s"
)


async def add_log(err):
    logging.error(str(err))

