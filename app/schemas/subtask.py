
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.usersummary import UserSummary


class Create(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(default="", max_length=500)
    completed: bool = False
    assigned_user_ids: list[int] = Field(min_length=1)
    task_id:int


class SubTaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = Field(default=None, min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool | None = None
    assigned_user_ids: list[int] | None = Field(default=None, min_length=1)


class SubTaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    completed: bool
    task_id: int
    assigned_user: list[UserSummary] = Field(default_factory=list)