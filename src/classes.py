from pydantic import BaseModel

class User(BaseModel):
    user_id: str | None
    username: str | None
    green_scores: int | None


class Post(BaseModel):
    post_id: int | None
    post_name: str | None
    post_description: str | None
    post_type: str | None
    status: str | None
    trade_id: int | None
    photos: list | None
    categories: list | None