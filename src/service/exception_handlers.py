from fastapi.responses import JSONResponse
from fastapi import Request
from src.service.exceptions import (
    ParentException
)

async def parent_exception_handler(request: Request, exc: ParentException) -> JSONResponse:
    ...
