import re
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str):
        value = " ".join(value.split())
        if len(value.split()) < 2:
            raise ValueError("full_name phải có ít nhất 2 từ")
        return value


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=72)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str):
        if not re.search(r"[@#$%!]", value):
            raise ValueError("Mật khẩu phải có ít nhất 1 ký tự đặc biệt: @, #, $, %, !")
        return value


class UserUpdate(BaseModel):
    full_name: str | None = Field(None, min_length=1, max_length=255)
    is_active: bool | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    role: str
    is_active: bool
    created_at: datetime


class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr


class UserInfoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: str


class MeResponse(UserResponse):
    is_admin: bool
    account_age_days: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    device_name: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_info: UserInfoResponse


class RefreshRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
