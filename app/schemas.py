from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional


class SubsystemSchema(BaseModel):
    id: int
    name: str
    project_id: int
    platform_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ProjectSchema(BaseModel):
    id: int
    name: str
    subsystems: list[SubsystemSchema] = []

    model_config = ConfigDict(from_attributes=True)


class PlatformSchema(BaseModel):
    id: int
    name: str
    projects: list[ProjectSchema] = []

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str  # Staff Number
    password: str
    remember_me: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    full_name: Optional[str] = None
    department: Optional[str] = None


class UserSchema(BaseModel):
    id: int
    username: str
    staff_number: str
    role: str
    is_active: bool
    is_approved: bool
    department: Optional[str] = None
    role_designation: Optional[str] = None

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
