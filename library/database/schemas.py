from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    email: str
    password_hash: str
    is_admin: bool
    images: list["Image"]
    settings: set["Setting"]


class Setting(BaseModel):
    id: str
    user: "User"
    image_expiry: int


class Image(BaseModel):
    id: str
    image_hash: str
    image_name: str
    expiry_time = int
    user_id: str
    user: "User"
