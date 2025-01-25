from fastapi import status, HTTPException
import inspect
import sys


class ParentException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Internal Server Error'
    reason = None

    def __init__(self, reason: str = None):
        self.reason = reason

    def __str__(self):
        return self.reason if self.reason else self.detail


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


class PostBlocked(ParentException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Post blocked'


class TradeNotFound(ParentException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Trade not found'


class OfferNotFound(ParentException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Offer not found'


class OfferAlreadyExists(ParentException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Offer already exists'


class NotYours(ParentException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Not Yours'


class NotVerificated(ParentException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = 'Not Verified'


class CategoryNotFound(ParentException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Category not found'
