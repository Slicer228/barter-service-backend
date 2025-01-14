from fastapi import status, HTTPException


class ParentException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Internal Server Error'
    reason = None

    def __init__(self, reason: str = None):
        self.reason = reason
        super().__init__(status_code=self.status_code, detail=self.detail)

    def __str__(self):
        return self.reason


class UserNotFound(ParentException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'User not found'


class UserAlreadyExists(ParentException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'User already exists'


class CannotInteractWithSelf(ParentException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Cannot interact with self'


class UserBlocked(ParentException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'User blocked'

class UserUnauthorized(ParentException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Unauthorized'


class PostNotFound(ParentException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class PostBlocked(ParentException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Post blocked'


class TradeNotFound(ParentException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Trade not found'