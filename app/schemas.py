from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str
    remember_me: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

class UserSchema(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
