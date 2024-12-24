from typing import Optional
from pydantic import EmailStr, BaseModel


class SchemaPostPhoto(BaseModel):
    post_photo: str
    post_photo_name: str
class SchemaAddPost(BaseModel):
    user_id: int
    post_name: str
    post_type: str
    post_description: str | None = None
    photos: list[SchemaPostPhoto] | None = None
    categories: list[int]

class SchemaAddUser:
    username: str
    password: str
    email: EmailStr
    avatar: str | None = None

class SchemaActOffer:
    post_id: int
    source_post_id: int
    user_id: int | None = None