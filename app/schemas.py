from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    username: str # Staff Number
    password: str
    remember_me: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

class UserSchema(BaseModel):
    id: int
    username: str
    staff_number: str
    role: str
    is_active: bool
    is_approved: bool

    model_config = ConfigDict(from_attributes=True)

class UserRegister(BaseModel):
    staff_number: str
    password: str
    full_name: str
    department: str
    role_designation: str
    dob: str
    phone_number: str
    personal_email: str
    official_email: str
