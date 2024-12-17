from enum import Enum


class UserResponse:
    NOT_FOUND = {'status_code': 404, 'detail': 'User not found'}
    ERROR = {'status_code': 500, 'detail': 'Server error'}
    ALREADY_EXISTS = {'status_code': 400, 'detail': 'User already exists'}
    BLOCKED = {'status_code': 403, 'detail': 'Forbidden'}

class PostResponse:
    NOT_FOUND = {'status_code': 404, 'detail': 'Post not found'}
    ERROR = {'status_code': 500, 'detail': 'Server error'}
    BLOCKED = {'status_code': 403, 'detail': 'Forbidden'}
