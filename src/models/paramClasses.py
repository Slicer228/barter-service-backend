from typing import Optional


class SchemaAddPost:
    def __init__(
            self,
            user_id: str,
            post_name: str,
            post_description: Optional[str],
            post_type: str,
            photos: Optional[list] = None,
            categories: Optional[list[str]] = None
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
            avatar: str | None = None
    ):
        self.password = password
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