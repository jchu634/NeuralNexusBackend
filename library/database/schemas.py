from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    password_hash: str
    is_admin: bool