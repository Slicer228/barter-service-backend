from pydantic import EmailStr, BaseModel


class SchemaPostPhoto(BaseModel):
    post_photo: str
    post_photo_name: str


class SchemaAddPost(BaseModel):
    post_name: str
    post_type: str
    post_description: str | None = None
    photos: list[SchemaPostPhoto] | None = None
    categories: list[int]


class SchemaAddUser(BaseModel):
    username: str
    password: str
    email: EmailStr
    avatar: str | None = None


class SchemaAuthUser(BaseModel):
    email: EmailStr
    password: str


class SchemaSendOffer(BaseModel):
    trade_id: int
    source_post_id: int = 0
