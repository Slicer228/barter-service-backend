from pydantic import BaseModel


class PostFilterSchema(BaseModel):
    categories: list[int] | None = None
    categories_strict_flag: bool | None = None
