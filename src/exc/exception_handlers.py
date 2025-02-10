from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import Response, Request
from fastapi.exceptions import RequestValidationError, ResponseValidationError


async def validations_req_err(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({'detail': exc, 'error': 'bad request'})
    )


async def validations_resp_err(response: Response, exc: ResponseValidationError):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder({'detail': exc.errors(), 'error': 'bad response'})
    )


constructors = [
    (ResponseValidationError, validations_resp_err),
    (RequestValidationError, validations_req_err)
]
