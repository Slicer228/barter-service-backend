from fastapi import status, HTTPException


class ParentException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Internal Server Error'

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class UserNotFound(ParentException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'User not found'

class UserAlreadyExists(ParentException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'User already exists'

class UserBlocked(ParentException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'User blocked'

class UserUnauthorized(ParentException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Unauthorized'

class PostNotFound(ParentException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Post not found'

class PostBlocked(ParentException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Post blocked'