from enum import Enum
from starlette import status
import fastapi


class UserResponse:
    NOT_FOUND = {'status_code': 404, 'detail': 'User not found'}
    ERROR = {'status_code': 500, 'detail': 'Server error'}
    ALREADY_EXISTS = {'status_code': 400, 'detail': 'User already exists'}
    BLOCKED = {'status_code': 403, 'detail': 'Forbidden'}
    AUTH_ERROR = {'status_code': 400, 'detail': 'Auth error'}
    NOT_AUTH = {'status_code': 401, 'detail': 'Unaauthorized'}

class PostResponse:
    NOT_FOUND = {'status_code': 404, 'detail': 'Post not found'}
    ERROR = {'status_code': 500, 'detail': 'Server error'}
    BLOCKED = {'status_code': 403, 'detail': 'Forbidden'}
