from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, BLOB, Column, TIMESTAMP, Boolean
from typing import List, Optional
from datetime import date


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(16), nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    avatar: Mapped[str] = mapped_column(BLOB, default=None)
    green_scores: Mapped[int] = mapped_column(Integer, default=0)
    green_points: Mapped[int] = mapped_column(Integer, default=0)
    verificated: Mapped[bool] = mapped_column(Boolean, default=False)
    refresh_token: Mapped[str] = mapped_column(String(256), default=None)


class UserPosts(Base):
    __tablename__ = 'user_posts'

    post_id: Mapped[int] = mapped_column(primary_key=True,unique=True,autoincrement=True)
    post_name: Mapped[str] = mapped_column(String(32), nullable=False)
    post_description: Mapped[str] = mapped_column(String(1024), default='Пользователь не оставил описания')
    post_type: Mapped[str] = mapped_column(String(5), nullable=False)
    trade_id: Mapped[int] = mapped_column(Integer, ForeignKey('trades.trade_id'), nullable=False)
    post_status: Mapped[str] = mapped_column(String(10), nullable=False, default='active')


class Categories(Base):
    __tablename__ = 'categories'

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True,unique=True)
    category_name: Mapped[str] = mapped_column(String(32), nullable=False)
    green_score: Mapped[int] = mapped_column(Integer, nullable=False)


class PostCategories(Base):
    __tablename__ = 'post_categories'

    post_id: Mapped[int] = mapped_column(ForeignKey('user_posts.post_id'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.category_id'), nullable=False)
    category_type: Mapped[str] = mapped_column(String(16), nullable=False, primary_key=True)

    category_names = relationship(
        'Categories',
        primaryjoin="PostCategories.category_id == Categories.category_id"
    )


class Trades(Base):
    __tablename__ = 'trades'

    trade_id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True, unique=True)
    date: Mapped[date] = mapped_column(TIMESTAMP, nullable=False)


class UserTrades(Base):
    __tablename__ = 'user_trades'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)  # surrogate column
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.user_id'), nullable=False)
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_posts.post_id'), nullable=False)
    trade_id: Mapped[int] = mapped_column(Integer, ForeignKey('trades.trade_id'), nullable=False)
    utType: Mapped[str] = mapped_column(String(6), nullable=False)
    trade_status: Mapped[str] = mapped_column(String(10), nullable=False, default='active')


class PostPhotos(Base):
    __tablename__ = 'post_photos'

    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_posts.post_id'), nullable=False)
    post_photo: Mapped[str] = mapped_column(BLOB, nullable=False)
    post_photo_name: Mapped[str] = mapped_column(String(32), nullable=False, primary_key=True)


class EmailVerification(Base):
    __tablename__ = 'email_verification'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    secret_code: Mapped[str] = mapped_column(String(100), default=None)
    expiration_time: Mapped[date] = mapped_column(TIMESTAMP, default=None)

