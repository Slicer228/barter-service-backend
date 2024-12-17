from typing import Optional
from pydantic import EmailStr

class SchemaAddPost:
    def __init__(
            self,
            user_id: int,
            post_name: str,
            post_type: str,
            post_description: str | None = None,
            photos: list | None = None,
            categories: list[str] | None = None
    ):
        self.user_id = user_id
        self.post_name = post_name
        self.post_description = post_description
        self.post_type = post_type
        self.photos = photos
        self.categories = categories

class SchemaAddUser:
    def __init__(
            self,
            username: str,
            password: str,
            email: EmailStr,
            avatar: str | None = None
    ):
        self.password = password
        self.email = email
        self.avatar = avatar
        self.username = username

class SchemaActOffer:
    def __init__(
            self,
            post_id: int,
            source_post_id: int,
            user_id: Optional[str] = None
    ):
        self.post_id = post_id
        self.source_post_id = source_post_id
        self.user_id = user_id