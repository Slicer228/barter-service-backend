from pydantic import BaseModel


class SchemaUser(BaseModel):
    user_id: int
    username: str
    avatar: str | None
    green_scores: int
    green_points: int

class SchemaPostPhoto(BaseModel):
    post_photo_name: str
    post_photo: str

class SchemaPost(BaseModel):
    owner: SchemaUser | None
    post_id: int
    post_name: str
    post_description: str | None
    post_type: str
    status: str
    photos: list[SchemaPostPhoto] | list
    categories: list[int] | list


class SchemaOffer(BaseModel):
    post: SchemaPost
    from_user: SchemaUser
    source_post: SchemaPost
