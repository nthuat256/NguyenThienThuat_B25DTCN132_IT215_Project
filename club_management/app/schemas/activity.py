from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ActivityBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = None
    assignee_id: int | None = None
    status: str = Field("TODO", max_length=30)
    priority: str = Field("MEDIUM", max_length=20)
    due_date: datetime | None = None

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    assignee_id: int | None = None
    status: str | None = Field(None, max_length=30)
    priority: str | None = Field(None, max_length=20)
    due_date: datetime | None = None

class ActivityResponse(ActivityBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    club_id: int
    created_at: datetime