from pydantic import BaseModel

import uuid
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass

# class User(BaseModel):
#     id: str
#     username: str
#     email: str
#     password_hash: str
#     is_admin: bool
#     images: list["Image"]
#     settings: set["Setting"]


# class Setting(BaseModel):
#     id: str
#     user: "User"
#     image_expiry: int


# class Image(BaseModel):
#     id: str
#     image_hash: str
#     image_name: str
#     expiry_time = int
#     user_id: str
#     user: "User"
