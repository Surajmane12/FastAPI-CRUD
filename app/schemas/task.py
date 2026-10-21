
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.usersummary import UserSummary
from app.schemas.subtask import SubTaskRead


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=500)
    completed: bool = False
    assigned_user_ids: list[int] = Field(min_length=1)


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool | None = None
    assigned_user_ids: list[int] | None = Field(default=None, min_length=1)


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    completed: bool
    created_At: datetime
    assigned_user: list[UserSummary]
    subtasks:list[SubTaskRead]= Field(default_factory=list)
