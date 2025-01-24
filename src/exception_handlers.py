from src.exceptions import *
from sqlalchemy.exc import IntegrityError
from src.utils import addLog
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Request
from src.exceptions import (
    ParentException,
    UserNotFound,
    UserAlreadyExists,
    CannotInteractWithSelf,
    UserUnauthorized,
    UserBlocked,
    PostBlocked,
    PostNotFound,
    TradeNotFound,
    OfferNotFound,
    OfferAlreadyExists,
    NotYours
)

async def parent_exception_handler(request: Request, exc: ParentException) -> JSONResponse:
    ...
