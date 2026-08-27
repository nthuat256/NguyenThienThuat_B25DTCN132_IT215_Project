from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


ClubMemberRole = Literal["MEMBER", "MODERATOR"]


class ClubBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("name không được để trống")
        return value


class ClubCreate(ClubBase):
    pass


class ClubUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("name không được để trống")
        return value


class ClubMemberCreate(BaseModel):
    user_id: int = Field(ge=1)
    role: ClubMemberRole = "MEMBER"


class ClubMemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    club_id: int
    user_id: int
    role: str
    joined_at: datetime


class ClubResponse(ClubBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    created_at: datetime