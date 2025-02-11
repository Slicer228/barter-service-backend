from pydantic import EmailStr, BaseModel


class AddPostPhotoSchema(BaseModel):
    post_photo: str
    post_photo_name: str


class AddPostSchema(BaseModel):
    post_name: str
    post_type: str
    post_description: str | None = None
    photos: list[AddPostPhotoSchema] | None = None
    categories: list[int]


class RegisterUserSchema(BaseModel):
    username: str
    password: str
    email: EmailStr
    avatar: str | None = None


class AuthenticateUserSchema(BaseModel):
    email: EmailStr
    password: str


class RequestTradeDataSchema(BaseModel):
    trade_id: int
    source_post_id: int = 0
