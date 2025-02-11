from pydantic import BaseModel


class UserSchema(BaseModel):
    user_id: int
    username: str
    avatar: str | None
    green_scores: int
    green_points: int


class PostPhotoSchema(BaseModel):
    post_photo_name: str
    post_photo: str


class PostSchema(BaseModel):
    owner: UserSchema | None
    post_id: int
    trade_id: int
    post_name: str
    post_description: str | None
    post_type: str
    status: str
    photos: list[PostPhotoSchema] | list
    categories: list[int]


class TradeSchema(BaseModel):
    post: PostSchema
    source_post: PostSchema | UserSchema
