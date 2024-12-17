from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, BLOB, Column, TIMESTAMP
from typing import List, Optional
from datetime import date


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username: Mapped[str] = mapped_column(String(16),nullable=False)
    password: Mapped[str] = mapped_column(String(128),nullable=False)
    email: Mapped[str] = mapped_column(String(32),nullable=False,unique=True)
    avatar: Mapped[str] = mapped_column(BLOB,default=None)
    green_scores: Mapped[int] = mapped_column(Integer,default=0)
    green_points: Mapped[int] = mapped_column(Integer,default=0)

class User_posts(Base):
    __tablename__ = 'user_posts'

    post_id: Mapped[int] = mapped_column(primary_key=True,unique=True,autoincrement=True)
    post_name: Mapped[str] = mapped_column(String(32),nullable=False)
    post_description: Mapped[str] = mapped_column(String(1024),default='Пользователь не оставил описания')
    post_type: Mapped[str] = mapped_column(String(5),nullable=False)
    trade_id: Mapped[int] = mapped_column(Integer,ForeignKey('trades.trade_id'),nullable=False)
    status: Mapped[str] = mapped_column(String(7),nullable=False,default='active')


class Categories(Base):
    __tablename__ = 'categories'

    category_id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True,unique=True)
    category_name: Mapped[str] = mapped_column(String(32),nullable=False)
    green_score: Mapped[int] = mapped_column(Integer,nullable=False)

class Post_categories(Base):
    __tablename__ = 'post_categories'

    post_id: Mapped[int] = mapped_column(ForeignKey('user_posts.post_id'),nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.category_id'),nullable=False)
    category_type: Mapped[str] = mapped_column(String(16),nullable=False,primary_key=True)

    category_names = relationship(
        'Categories',
        primaryjoin="Post_categories.category_id == Categories.category_id"
    )

class Trades(Base):
    __tablename__ = 'trades'

    trade_id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,unique=True)
    date: Mapped[date] = mapped_column(TIMESTAMP,nullable=False)

class User_trades(Base):
    __tablename__ = 'user_trades'

    user_id: Mapped[int] = mapped_column(Integer,ForeignKey('users.user_id'),nullable=False)
    post_id: Mapped[int] = mapped_column(Integer,ForeignKey('users.post_id'),nullable=False)
    trade_id: Mapped[int] = mapped_column(Integer,ForeignKey('trades.trade_id'),nullable=False)
    utType: Mapped[str] = mapped_column(String(6),nullable=False,primary_key=True)

class Post_photos(Base):
    __tablename__ = 'post_photos'

    post_id: Mapped[int] = mapped_column(Integer,ForeignKey('user_posts.post_id'),nullable=False)
    post_photo: Mapped[str] = mapped_column(BLOB,nullable=False)
    post_photo_name: Mapped[str] = mapped_column(String(32),nullable=False,primary_key=True)