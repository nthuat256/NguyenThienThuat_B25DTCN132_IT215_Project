from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ClubBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None

class ClubCreate(ClubBase):
    pass

class ClubUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None

class ClubResponse(ClubBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    created_at: datetime

class ClubMemberBase(BaseModel):
    role: str = Field("MEMBER", max_length=20)

class ClubMemberCreate(ClubMemberBase):
    user_id: int

class ClubMemberResponse(ClubMemberBase):
    model_config = ConfigDict(from_attributes=True)
    club_id: int
    user_id: int
    joined_at: datetime